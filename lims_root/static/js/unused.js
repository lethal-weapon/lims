/**
 * Author: Jacob Wong
 * Date: 2020/4/13
 */

$(function () {

  // update account info when profile form submitted
  // $('#update-form').on('submit', function (e) {
  //   e.preventDefault();
  //   updateAccount($(this), $('#user-id').attr('value'));
  // });
});

// update the account info with ajax
function updateAccount(e, userID) {
  let url = e.attr('action').replace('\/0\/', '/' + userID + '/');
  // console.log(url);
  $.ajax({
    type:     "POST",
    url:      url,
    data:     e.serialize(),
    timeout:  2000,

    fail: function() {
      alert("fail to update the email");
    },
    success: function(data) {
      alert(data);
    },
    complete: function () {
      alert("It's done");
    }
  });
}