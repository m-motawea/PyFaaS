$(document).ready(function(){

     $('#logOut').on('click', function(){
        window.location = "index.html";

 });
//
    $('.carousel').carousel({
    interval:5000

    });
    $('#').on('click', function(){

    $.ajax({
      url: "myphp.php",
      data: {
          first: $("#myInput").val(),
          second: $("#myInputa").val(),
          third: $("#myInputb").val()
      },
      type: "POST"
  })
  .success(function (responseText, statusText, xhr) {
      console.log(xhr);
  })
  .fail(function (responseText, statusText, xhr) {
      console.log(xhr);
  });
});


});
// var socket = io('http://localhost');
    // socket.on('connect', function(){});
    // socket.on('event', function(data){});
    // socket.on('disconnect', function(){});

//add a new style 'foo'
// $.notify.addStyle('foo', {
//     html:
//       "<div>" +
//         "<div class='clearfix'>" +
//           "<div class='title' data-notify-html='title'/>" +
//           "<div class='buttons'>" +
//             "<button class='no'>Cancel</button>" +
//             "<button class='yes' data-notify-text='button'></button>" +
//           "</div>" +
//         "</div>" +
//       "</div>"
//   });

//   //listen for click events from this style
//   $(document).on('click', '.notifyjs-foo-base .no', function() {
//     //programmatically trigger propogating hide event
//     $(this).trigger('notify-hide');
//   });
//   $(document).on('click', '.notifyjs-foo-base .yes', function() {
//     //show button text
//     alert($(this).text() + " clicked!");
//     //hide notification
//     $(this).trigger('notify-hide');
//   });
