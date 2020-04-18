/**
 * Author: Jacob Wong
 * Date: 2020/4/11
 */

$(function () {
  updateGreeting();
  setClassForLinks();
});

// update the greeting according to current time
function updateGreeting() {
  let greeting;
  let hourNow = new Date().getHours();
  greeting = hourNow > 18 ? 'Good Evening' :
    (hourNow > 12 ? 'Good Afternoon' :
      (hourNow > 0 ? 'Good Morning' : 'Hi'));
  greeting += ',';

  $('#greeting').text(greeting);
}

// remove/add the 'current' class from/to
// the navigation links when they are clicked
function setClassForLinks() {
  let selector = '.navbar-home .mr-auto .nav-item > a';
  $(selector).on('click', function (e) {
    $(selector + '.current').removeClass('current');
    $(this).addClass('current');
  });

  // set class for current one
  let currentURL = window.location.href;
  $(selector).each(function () {
    let currentLink = $(this).attr('href');
    if (currentURL.indexOf(currentLink) >= 0) {
      $(this).addClass('current');
    }
  });
}
