/**
 * Author: Jacob Wong
 * Date: 2020/4/29
 */

$(function () {
  $('.application-table').DataTable();

  $('.btn-action').on('click', function () {
    ajaxApplication($(this).attr('data-action'), $(this).closest('form'));
  });

  $('.btn-remove').on('click', function () {
    removeFromList(
      $(this),
      $(this).closest('form').attr('data-remove-url'),
      $(this).closest('form').attr('data-facility-app-id'),
      $(this).attr('data-facility-id'));
  });
});

// All bottom buttons' action on application detail window
function ajaxApplication(action, form) {
  $.ajax({
    url: form.attr('data-ajax-url'),
    data: form.serialize() + '&action=' + action
      + '&type=' + form.attr('data-application-type'),
    timeout: 2000,
    dataType: 'json',

    success: function (data) {
      switch (action) {
        case 'APPLY': {
          if (data['is_success']) {
            // refresh my list page
            window.location.replace(window.location.href);
          } else {
            let selector = '#apply-message-' + data['id'];
            $(selector + ' > span').html(data['message'].replace(/\/\//g, '<br\/>'));
            $(selector).fadeIn(1000);
          }
          break;
        }
        case 'UPDATE': {
          if (data['is_success']) {
            let selector = '#update-message-' + data['id'];
            $(selector).fadeIn(300);
            $(selector).fadeOut(3000);
          }
          break;
        }
        case 'WITHDRAW':
        case 'DELETE': {
          if (data['is_success']) {
            // refresh my list page
            window.location.replace(window.location.href);
          }
          break;
        }
        default:
          break;
      }
    }
  });
}

// Remove button action on fa detail window
function removeFromList(button, removeURL, facilityAppID, facilityID) {
  $.ajax({
    url: removeURL,
    data: {
      'facility_id': facilityID,
      'facility_app_id': facilityAppID
    },
    timeout: 2000,
    dataType: 'json',

    success: function (data) {
      if (data['is_success']) {
        $(button).closest('li').fadeOut(1000);
      }
    }
  });
}