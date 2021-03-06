/**
 * Author: Jacob Wong
 * Date: 2020/4/29
 */

$(function () {
  $('.application-table').DataTable();

  // search panel switcher
  $('.search-trigger').on('click', function () {
    $(this).fadeOut(500);
    let $searchPanel = $('#search-panel-' + $(this).closest('form').attr('data-research-app-id'));

    if ($(this).hasClass('fa-expand')) {
      $(this).switchClass('fa-expand', 'fa-compress');
      $(this).attr('title', 'Hide search panel');
      $searchPanel.fadeIn(1000);
    } else {
      $(this).switchClass('fa-compress', 'fa-expand');
      $(this).attr('title', 'Show search panel');
      $searchPanel.fadeOut(1000);
    }

    $(this).fadeIn(500);
  });

  // search control
  $('.search-input').on('change', function () {
    let text = $(this).val();
    let $form = $(this).closest('form');
    let id = $form.attr('data-research-app-id');
    let URL = $form.attr('data-ajax-account-url');
    let selector = '#search-result-container-' + id + ' > ul ';
    let action = 'SEARCH';

    if (text.length < 1) {
      $(selector + 'li').remove();
      $(selector).html('<li><h6 class="text-center text-dark">' +
        '<strong>:( &nbsp;GIVE ME SOMETHING TO SEARCH</strong></h6></li>');
    } else {
      searchAccount(action, id, text, URL, selector);
    }
  });

  setButtonTriggers();
});

// Set all buttons' click trigger
function setButtonTriggers() {
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

  // add/remove account to/from member list
  $('.btn-account-action').on('click', function () {
    accountAction(
      $(this),
      $(this).closest('form').attr('data-ajax-account-url'),
      $(this).attr('data-action'),
      $(this).attr('data-account-id'),
      $(this).closest('form').attr('data-research-app-id')
    );
  });
}

// Account search control
function searchAccount(action, researchAppID, searchText,
                       searchURL, containerSelector) {
  $.ajax({
    url: searchURL,
    data: {
      'id': researchAppID,
      'text': searchText,
      'action': action
    },
    timeout: 2000,
    dataType: 'json',

    success: function (data) {
      let matchedList = '';
      $.each(data, function (key, val) {
        matchedList += '<li><h6 class="text-secondary"><i class="fa fa-user"></i>&nbsp; ';
        matchedList += val.fields.name + ' / ' + val.fields.campus_id + ' / ' + val.fields.school;
        matchedList += '<button type="button" class="btn btn-warning btn-sm btn-account-action pull-right hvr-grow" ';
        matchedList += 'data-action="ADD" data-account-id="' + val.pk + '">';
        matchedList += '<i class="fa fa-plus-circle"></i> Add</button></h6></li>';
      });

      // no matches
      if (matchedList.length < 1) {
        matchedList += '<li><h6 class="text-center text-dark">' +
          '<strong>:( &nbsp;NO MATCH FOUND</strong></h6></li>';
      }
      // remove old content, insert new ones, show up from top down
      $(containerSelector + 'li').remove();
      $(containerSelector).html(matchedList);
      $(containerSelector + 'li').hide().each(function (index) {
        $(this).fadeIn(500 * index);
      });
      setButtonTriggers();
    }
  });
}

function accountAction(button, URL, action,
                       accountID, researchAppID) {
  $.ajax({
    url: URL,
    data: {
      'id': researchAppID,
      'account_id': accountID,
      'action': action
    },
    timeout: 2000,
    dataType: 'json',

    success: function (data) {
      if (data['is_success']) {
        let $newMemberItem = $(button).closest('li');
        $newMemberItem.fadeOut(1000);

        // if it's a add action, move this item from search panel
        // to member panel after turning its add button into remove button
        if (action === 'ADD') {
          let $memberButton = $newMemberItem.find('button');
          $memberButton.attr('data-action', 'REMOVE');
          $memberButton.html('<i class="fa fa-remove"></i> Remove');

          let selector = '#member-container-' + researchAppID + ' > ul';
          $(selector).append($newMemberItem);
          $newMemberItem.fadeIn(1000);
        }
      } else {
        $('#apply-message-' + researchAppID + ' > span').text('Server Error');
      }
    }
  });
}

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