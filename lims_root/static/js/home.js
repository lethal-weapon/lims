/**
 * Author: Jacob Wong
 * Date: 2020/4/11
 */

$(function () {
  updateGreeting();
  setClassForLinks();

  $('#update-email-form').on('submit', function (e) {
    e.preventDefault();
    updateEmailAddress($(this));
  });
});

// Update the greeting according to current time
function updateGreeting() {
  let greeting;
  let hourNow = new Date().getHours();
  greeting = hourNow > 18 ? 'Good Evening' :
    (hourNow > 12 ? 'Good Afternoon' :
      (hourNow > 0 ? 'Good Morning' : 'Hi'));
  greeting += ',';

  $('#greeting').text(greeting);
}

// Remove/add the 'current' class from/to
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
    let currentLink = $(this).attr('href').toString();
    let linkPrefix = currentLink.split('/')[1];

    if (currentURL.indexOf(linkPrefix) >= 0) {
      $(this).addClass('current');
    }
  });
}

// Update email address
function updateEmailAddress(form) {
  $.ajax({
    url: $(form).attr('action'),
    data: $(form).serialize(),
    timeout: 2000,
    dataType: 'json',

    success: function (data) {
      let selector = '#email-update-message';
      $(selector + ' > span').text(data['message']);

      if (data['is_success']) {
        $(selector).switchClass('text-danger', 'text-success');
        $(selector + ' > i').switchClass('fa-exclamation-circle', 'fa-check');
        $('#table-email').text($('#form-email').val());
      } else {
        $(selector).switchClass('text-success', 'text-danger');
        $(selector + ' > i').switchClass('fa-check', 'fa-exclamation-circle');
      }

      $(selector).fadeIn(1000);
      $(selector).fadeOut(5000);
    }
  });
}