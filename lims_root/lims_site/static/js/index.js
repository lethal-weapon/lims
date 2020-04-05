/**
 * Author: Jacob Wong
 * Date: 2020/4/6
 */

$(function() {
  // fade in the three roles from left to right
  $('div.col-4').hide().each(function(index) {
    $(this).delay(300 * index).fadeIn();
  });
});
