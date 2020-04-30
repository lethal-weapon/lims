/**
 * Author: Jacob Wong
 * Date: 2020/4/29
 */

$(function () {
  $('.application-table').DataTable();

  $('.btn-save').on('click', function () {
    saveApplication($(this).closest('form'));
  });

  $('.btn-delete').on('click', function () {
    deleteApplication($(this).closest('form'));
  });

  $('.btn-remove').on('click', function () {
    removeFromList(
      $(this),
      $(this).closest('form').attr('data-remove-url'),
      $(this).closest('form').attr('data-facility-app-id'),
      $(this).attr('data-facility-id'));
  });
});

// Save button action
function saveApplication(form) {
  $.ajax({
    url: form.attr('data-update-url'),
    data: form.serialize(),
    timeout: 2000,
    dataType: 'json',

    success: function (data) {
      let selector = '#update-message-' + data['id'];
      $(selector).fadeIn(300);
      $(selector).fadeOut(3000);
    }
  });
}

// Delete button action
function deleteApplication(form) {
  $.ajax({
    url: form.attr('data-delete-url'),
    data: form.serialize(),
    timeout: 2000,
    dataType: 'json',

    // refresh my list page
    success: function (data) {
      window.location.replace(window.location.href);
    }
  });
}

// Remove button action
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