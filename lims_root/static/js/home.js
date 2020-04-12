/**
 * Author: Jacob Wong
 * Date: 2020/4/11
 */

$(function () {

  updateGreeting();

  setClassForLinks();

  // update account info when profile form submitted
  // $('#update-form').on('submit', function (e) {
  //   e.preventDefault();
  //   updateAccount($(this), $('#user-id').attr('value'));
  // });
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
}

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