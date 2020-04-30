/**
 * Author: Jacob Wong
 * Date: 2020/4/30
 */

$(function () {
  $('table.inventory-table').DataTable();

  $('.btn-add').on('click', function () {
    addToList(
      $(this),
      $(this).closest('form').attr('data-add-url'),
      $(this).closest('form').attr('data-facility-id'),
      $(this).attr('data-facility-app-id'));
  });
});

// Add button action
function addToList(button, addURL, facilityID, facilityAppID) {
  $.ajax({
    url: addURL,
    data: {
      'facility_id': facilityID,
      'facility_app_id': facilityAppID
    },
    timeout: 2000,
    dataType: 'json',

    success: function (data) {
      if (data['is_success']) {
        $(button).fadeOut(500);
        $(button).prev().switchClass(
          "fa-times text-dark", "fa-check text-success")
      }
    }
  });
}
