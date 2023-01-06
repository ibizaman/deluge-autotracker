/**
 * Script: autotracker.js
 *     The client-side javascript code for the autotracker plugin.
 *
 * Copyright:
 *     (C) pierre 2023 <deluge@pierre.tiserbox.com>
 *
 *     This file is part of autotracker and is licensed under GNU GPL 3.0, or
 *     later, with the additional special exception to link portions of this
 *     program with the OpenSSL library. See LICENSE for more details.
 */

autotrackerPlugin = Ext.extend(Deluge.Plugin, {
    constructor: function(config) {
        config = Ext.apply({
            name: 'autotracker'
        }, config);
        autotrackerPlugin.superclass.constructor.call(this, config);
    },

    onDisable: function() {
        deluge.preferences.removePage(this.prefsPage);
    },

    onEnable: function() {
        this.prefsPage = deluge.preferences.addPage(
            new Deluge.ux.preferences.autotrackerPage());
    }
});
new autotrackerPlugin();
