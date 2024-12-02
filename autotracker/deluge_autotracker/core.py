# -*- coding: utf-8 -*-
# Copyright (C) 2023 pierre <deluge@pierre.tiserbox.com>
#
# Basic plugin template created by the Deluge Team.
#
# This file is part of autotracker and is licensed under GNU GPL 3.0, or later,
# with the additional special exception to link portions of this program with
# the OpenSSL library. See LICENSE for more details.
from __future__ import unicode_literals

import logging
import threading
import time

import deluge.component as component
import deluge.configmanager
from deluge.plugins.pluginbase import CorePluginBase

log = logging.getLogger(__name__)

DEFAULT_PREFS = {
}


class Core(CorePluginBase):
    def enable(self):
        self.config = deluge.configmanager.ConfigManager(
            'autotracker.conf', DEFAULT_PREFS)

        self._timer = RepeatedTimer(5, checkSpeed, self.config)

    def disable(self):
        self._timer.stop()


def checkSpeed(config):
    ts = component.get('TorrentManager').torrents
    for torrent_id, torrent in ts.items():
        log.debug(
            "%s: download rate=%d, peers=%d, last seen complete=%d",
            torrent.get_name(),
            torrent.status.download_payload_rate,
            torrent.status.num_peers,
            int(time.time() - torrent.status.last_seen_complete),
        )
        if torrent.status.download_payload_rate < 0.1 and torrent.status.num_peers < 1:
            if torrent_id in config and len(config[torrent_id]) > 0:
                log.info("Adding back %d trackers for %s", len(config[torrent_id]), torrent.get_name())
                # set_trackers with len > 0 forces reannounce
                torrent.set_trackers(config[torrent_id])
                del config[torrent_id]
                config.save()
        else:
            if len(torrent.trackers) > 0:
                log.info("Removing %d trackers for %s", len(torrent.trackers), torrent.get_name())
                config[torrent_id] = torrent.trackers
                config.save()
                torrent.set_trackers([])


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.next_call += self.interval
            self._timer = threading.Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
