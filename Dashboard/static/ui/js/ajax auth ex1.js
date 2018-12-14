

var userEmail = $("input#username").val();
var userPassword = $("input#password").val();
var authToken

$(function(){
  login()
})
function login(){
  $.ajax({
    type: "POST",
    url: 'http://localhost:5000/login/',
    data: { user: { email: userEmail, password: userPassword } },
    success: function(response) {
      console.log('response => ', response)
      //login success! save the auth token and access some secret content
      authToken = response.auth_token
      getContent()
    },
    error: function (xhr, ajaxOptions, thrownError) {
        console.log(xhr.status);
        console.log(thrownError);
      }
  })
}

function getContent() {
  $.ajax({
    type: "GET",
    url: 'http://localhost:5000/login/',
    beforeSend: function (xhr)
    {
      // Using custom headers
      xhr.setRequestHeader("User-Email", userEmail)
      xhr.setRequestHeader("Auth-Token", authToken)
      // or Using http basic Authorization header
      // xhr.setRequestHeader ("Authorization", "Basic " + btoa(userEmail + ":" + authToken));
      
      // Remember that our server will need to accept those headers to avoid CORS issues
    },
    success: function(response) {
      console.log('response => ', response)
    },
    error: function (xhr, ajaxOptions, thrownError) {
        console.log(xhr.status);
        console.log(thrownError);
      }
  })
}
