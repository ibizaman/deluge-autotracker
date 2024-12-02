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

Deluge.plugins.AutotrackerPlugin = Ext.extend(Deluge.Plugin, {
    name: 'Autotracker',

    static: {
        prefsPage: null,
    },

    onDisable: function () {
        deluge.preferences.removePage(Deluge.plugins.AutotrackerPlugin.prefsPage);
        Deluge.plugins.AutotrackerPlugin.prefsPage = null;
    },

    onEnable: function () {
        /*
         * Called for each of the JavaScript files.
         * This will prevent adding unnecessary tabs to the preferences window.
         */
        if (!Deluge.plugins.AutotrackerPlugin.prefsPage) {
            Deluge.plugins.AutotrackerPlugin.prefsPage = deluge.preferences.addPage(
                new Deluge.ux.preferences.autotrackerPage()
            );
        }
    },
});

Deluge.registerPlugin('AutoAdd', Deluge.plugins.AutotrackerPlugin);
