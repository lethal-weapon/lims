/**
 * Author: Jacob Wong
 * Date: 2020/4/11
 */

$(function () {
  setClassForLinks();

  // update the greeting according to current hour
  let greeting;
  let hourNow = new Date().getHours();
  greeting = hourNow > 18 ? 'Good Evening' :
    (hourNow > 12 ? 'Good Afternoon' :
      (hourNow > 0 ? 'Good Morning' : 'Hi'));
  greeting += ',';

  $('#greeting').text(greeting);
});

// remove/add the 'current' class from/to
// the navigation links when they are clicked
function setClassForLinks() {
  let selector = ".navbar-home .mr-auto .nav-item > a";
  $(selector).on('click', function(e) {
      $(selector + ".current").removeClass('current');
      $(this).addClass('current');
  });
}
