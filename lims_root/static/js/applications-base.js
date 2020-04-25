/**
 * Author: Jacob Wong
 * Date: 2020/4/25
 */

$(function () {
  setIconForLinks();
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