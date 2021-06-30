// ==UserScript==
// @name         HookBase64
// @namespace   https://scrape.center/
// @version     0.1
// @description Hook Base64 encode function
// @author       Germey
// @match       https://dynamic6.scrape.center/
// @grant       none
// @run-at     document-start
// ==/UserScript==
(function () {
    'use strict'

    function hook(object, attr) {
        var func = object[attr]
        console.log('func', func)
        object[attr] = function () {
            console.log('hooked', object, attr)
            var ret = func.apply(object, arguments)
            debugger
            return ret
        }
    }

    hook(window, 'btoa')
})()