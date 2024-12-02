# -*- coding: utf-8 -*-
# Copyright (C) 2023 pierre <deluge@pierre.tiserbox.com>
#
# Basic plugin template created by the Deluge Team.
#
# This file is part of autotracker and is licensed under GNU GPL 3.0, or later,
# with the additional special exception to link portions of this program with
# the OpenSSL library. See LICENSE for more details.

import logging

from deluge.plugins.pluginbase import WebPluginBase

from .common import get_resource

log = logging.getLogger(__name__)


class WebUI(WebPluginBase):

    scripts = [get_resource('autotracker.js')]

    def enable(self):
        pass

    def disable(self):
        pass
