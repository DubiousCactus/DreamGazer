/*
 * index.js
 * Copyright (C) 2018 transpalette <transpalette@translaptop>
 *
 * Distributed under terms of the MIT license.
 */
(function(){
  'use strict';
  
   $('#start').click(function(e) {
   	   console.log('clicked');
   	   $('#header').slideToggle(500, function() {
   	   	   console.log('slideToggle');
	   });
   });
})();
