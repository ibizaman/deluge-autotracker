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

import deluge.component as component
import deluge.configmanager
from deluge.core.rpcserver import export
from deluge.plugins.pluginbase import CorePluginBase

log = logging.getLogger(__name__)

DEFAULT_PREFS = {
}


class Core(CorePluginBase):
    def enable(self):
        self.__handlers__ = {
            'TorrentStateChangedEvent': self.on_statechanged,
            'TorrentTrackerStatusEvent': self.on_trackerstatus,
            'TorrentRemovedEvent': self.on_torrentremoved,
        }

        self.config = deluge.configmanager.ConfigManager(
            'autotracker.conf', DEFAULT_PREFS)

        event_manager = component.get('EventManager')
        for event, handler in self.__handlers__.items():
            event_manager.register_event_handler(event, handler)

    def disable(self):
        event_manager = component.get('EventManager')
        for event, handler in self.__handlers__.items():
            event_manager.deregister_event_handler(event, handler)

    def on_statechanged(self, torrent_id, state):
        if self._maybe_remove_trackers(torrent_id):
            return

        self._maybe_readd_trackers(torrent_id)

    def on_trackerstatus(self, torrent_id, tracker_status):
        self._maybe_remove_trackers(torrent_id)

    def on_torrentremoved(self, torrent_id):
        if torrent_id in self.config:
            del self.config[torrent_id]
            self.config.save()

    def update(self):
        pass

    def _torrent(self, torrent_id):
        ts = component.get('TorrentManager').torrents
        if torrent_id not in ts:
            return None
        return ts[torrent_id]

    def _maybe_readd_trackers(self, torrent_id):
        torrent = self._torrent(torrent_id)
        if torrent is None:
            return

        if torrent.state == "Seeding" and torrent_id in self.config and len(self.config[torrent_id]) > 0:
            if len(torrent.trackers) == 0 and len(self.config[torrent_id]) > 0:
                print("autotracker: adding back trackers for", torrent_id)
                torrent.set_trackers(self.config[torrent_id])
                del self.config[torrent_id]
                self.config.save()
            return True

        return False

    def _maybe_remove_trackers(self, torrent_id):
        torrent = self._torrent(torrent_id)
        if torrent is None:
            return False

        if torrent.state == "Downloading" and torrent.tracker_status == "Announce OK":
            print("autotracker: removing trackers for", torrent_id)
            if len(torrent.trackers) > 0:
                self.config[torrent_id] = torrent.trackers
                self.config.save()
            torrent.set_trackers([])
            return True

        return False

    @export
    def set_config(self, config):
        """Sets the config dictionary"""
        for key in config:
            self.config[key] = config[key]
        self.config.save()

    @export
    def get_config(self):
        """Returns the config dictionary"""
        return self.config.config
