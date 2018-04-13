/*
 * index.js
 * Copyright (C) 2018 transpalette <transpalette@translaptop>
 *
 * Distributed under terms of the MIT license.
 */
(function(){
  'use strict';
  
   $('#start').click(function(e) {
   	   $('#header').slideUp("slow", function() {
   	   	   $('#placeholder').fadeOut('fast');
		   $('.gaze').slideDown("slow");
			setTimeout(3, gaze());
	   });
   });


	function gaze() {
		webgazer.setGazeListener(function(data, elapsedTime) {
			if (data == null)
				return;

			var xprediction = data.x; //these x coordinates are relative to the viewport
			var yprediction = data.y; //these y coordinates are relative to the viewport
			console.log(xprediction, yprediction);
			console.log(elapsedTime); //elapsed time is based on time since begin was called
		}).begin();
	}
})();
