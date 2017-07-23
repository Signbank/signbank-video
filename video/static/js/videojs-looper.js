(function (global, factory) {
	typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory(require('video.js')) :
	typeof define === 'function' && define.amd ? define(['video.js'], factory) :
	(global.videojsLooper = factory(global.videojs));
}(this, (function (videojs) { 'use strict';

videojs = 'default' in videojs ? videojs['default'] : videojs;

var version = "0.0.0";

// Default options for the plugin.
var defaults = {};

// Cross-compatibility for Video.js 5 and 6.
var registerPlugin = videojs.registerPlugin || videojs.plugin;
// const dom = videojs.dom || videojs;

/**
 * Function to invoke when the player is ready.
 *
 * This is a great place for your plugin to initialize itself. When this
 * function is called, the player will have its DOM and child components
 * in place.
 *
 * @function onPlayerReady
 * @param    {Player} player
 *           A Video.js player object.
 *
 * @param    {Object} [options={}]
 *           A plain object containing options for the plugin.
 */
var onPlayerReady = function onPlayerReady(player, options) {
  player.addClass('vjs-looper');
};

/**
 * A video.js plugin.
 *
 * In the plugin function, the value of `this` is a video.js `Player`
 * instance. You cannot rely on the player being in a "ready" state here,
 * depending on how the plugin is invoked. This may or may not be important
 * to you; if not, remove the wait for "ready"!
 *
 * @function looper
 * @param    {Object} [options={}]
 *           An object of options left to the plugin author to define.
 */
var looper = function looper(options) {
  var _this = this;

  this.ready(function () {
    onPlayerReady(_this, videojs.mergeOptions(defaults, options));
    _this.getChild('controlBar').addChild('LoopButton');
  });
};

var Button = videojs.getComponent('Button');

// Extend default
var LoopButton = videojs.extend(Button, {
  constructor: function constructor(player, options) {
    Button.apply(this, arguments);
  },
  createEl: function createEl() {
    return Button.prototype.createEl('button', {
      className: 'vjs-looper-button',
      innerHTML: 'Loop'
    });
  },
  handleClick: function handleClick() {

    var player = this.player_;
    var btn = player.getChild('controlBar').getChild('LoopButton');

    if (player.options_.loop === true) {
      player.options_.loop = false;
      btn.removeClass('vjs-control-active');
    } else {
      player.options_.loop = true;
      btn.addClass('vjs-control-active');
    }
  }
});

// Register the new component
videojs.registerComponent('LoopButton', LoopButton);

// Register the plugin with video.js.
registerPlugin('looper', looper);

// Include the version number.
looper.VERSION = version;

return looper;

})));
