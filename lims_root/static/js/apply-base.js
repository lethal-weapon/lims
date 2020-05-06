/**
 * Author: Jacob Wong
 * Date: 2020/4/25
 */

$(function () {
  setIconForLinks();

  $('.create-form').on('submit', function (e) {
    e.preventDefault();
    createApplication($(this));
  });
});

// Finger icons are blocked by default
// Show the icon on left side of the current tab
function setIconForLinks() {
  let selector = '.sidebar nav ul li > i';
  let currentURL = window.location.href;

  $(selector).each(function (index) {
    let currentLink = $(this).next().attr('href');
    if (currentURL.indexOf(currentLink) >= 0) {
      $(this).show();
    }
  });
}

// Create an application
function createApplication(form) {
  $.ajax({
    url: form.attr('data-ajax-url'),
    data: form.serialize() + '&action=' + form.attr('data-action')
            + '&type=' + form.attr('data-application-type'),
    timeout: 2000,
    dataType: 'json',

    success: function (data) {
      let selector = '.create-message'
      $(selector + ' > strong').text(data['message']);

      if (data['is_success']) {
        $(selector).switchClass('alert-danger', 'alert-success');
      } else {
        $(selector).switchClass('alert-success', 'alert-danger');
      }

      $(selector).fadeIn(1000);
      $(selector).fadeOut(5000);
    }
  });
}