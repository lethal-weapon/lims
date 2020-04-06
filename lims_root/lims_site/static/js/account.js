/**
 * Author: Jacob Wong
 * Date: 2020/4/6
 */

$(function () {
  // fade in all form components from top down
  $('div.form-group').hide().each(function (index) {
    $(this).delay(200 * index).slideDown();
  });
});
