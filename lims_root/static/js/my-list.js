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
      $(selector).addClass('alert alert-success text-center');
      $(selector).text(data['message']);
      $(selector).fadeIn(300);
      $(selector).fadeOut(5000);
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