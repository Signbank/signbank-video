/* ! Loopbutton v1.0.0 Copyright 2014 Charlotte Dunois https://github.com/CharlotteDunois/videojs-loopbutton/blob/master/LICENSE.md ! */
videojs.plugin('loopbutton', function(options) {
	var player = this;

	var VjsButton = videojs.getComponent('Button');
	var LoopButton = videojs.extend(VjsButton, {

	  // The `init()` method will also work for constructor logic here, but it is
	  // deprecated. If you provide an `init()` method, it will override the
	  // `constructor()` method!
	  constructor: function() {
	    VjsButton.call(this, player, options);
	  }, // notice the comma

	  buttonText: 'Loop',

	  buildCSSClass: function() {
	  	return 'vjs-loop-button vjs-menu-button';
	  },

	  onClick: function(e){
  		if(player.options_['loop'] == true) {
  			player.options_['loop'] = false;
  			this.removeClass('vjs-control-active');
  		} else {
  			player.options_['loop'] = true;
  			this.addClass('vjs-control-active');
  		}
	  }
  });

	player.ready(function(){
		var button = new LoopButton(player);
		player.controlBar.addChild(button);

		player.on('ended', function() {
			if(player.options_['loop'] == true) {
				player.play();
			}
		});
	});
});
