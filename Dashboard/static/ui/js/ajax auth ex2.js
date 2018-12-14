// document.write("\<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js' type='text/javascript'>\<\/script>");

$(document).ready(function(){
 
         $("#logIn").click(function(){

                    var Surl="prof.html";
                    $(location).attr('href',Surl);
                    window.location = "./prof.html"; 
           
              });

        // });
    });

     // // window.addEventListener("load", function () {
            //     function sendData() {
            //       var XHR = new XMLHttpRequest();
              
            //       // Bind the FormData object and the form element
            //       var FD = new FormData(form);
              
            //       // Define what happens on successful data submission
            //       XHR.addEventListener("load", function(event) {
            //         alert(event.target.responseText);
            //       });
              
            //       // Define what happens in case of error
            //       XHR.addEventListener("error", function(event) {
            //         alert('Oops! Something went wrong.');
            //       });
              
            //       // Set up our request
            //       XHR.open("POST", "https://jsonplaceholder.typicode.com/posts");
              
            //       // The data sent is what the user provided in the form
            //       XHR.send(FD);
            //     }
               
            //     // Access the form element...
            //     var form = document.getElementById("myForm");
              
            //     // ...and take over its submit event.
            //     form.addEventListener("submit", function (event) {
            //       event.preventDefault();
              
            //       sendData();
            //     });
   /* $("#signUp").click(function(){

var userEmail = $("input#username").val();
var userPassword = $("input#password").val();
var authToken
var auth =btoa('userEmail:userPassword');

$(function(){
login()
})
function login(){
$.ajax({
type: "POST",
url: 'https://jsonplaceholder.typicode.com/posts',
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
url: 'https://jsonplaceholder.typicode.com/posts',
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
//success block
console.log('response => ', response)
},
error: function (xhr, ajaxOptions, thrownError) {
console.log(xhr.status);
console.log(thrownError);
}
})
}
        
});*/   

           /* var psw =$("input[name=psw]").val();
            var email=$("input[name=email]").val();
            $.getJSON("https://api.myjson.com/bins/13wbve",function(rText){
                $.each(rText,function(num,obj){
                   
                           // myOut=myOut+obj.email+'<BR>'+obj.password+'<BR>';
                    $("#output").html(myOut);                      
                jemail=obj.email;
                jpsw=obj.password;    
                    if( email == jemail && psw == jpsw){
                       
                        $(location).attr('href',url);

                    }

                })
                
            console.log(rText);    
                
            })*/
//             $.ajax({
//                 type: 'GET',
//                 url: 'https://api.myjson.com/bins/:q2zju',
//                 data: '{"username": "' + userEmail + '", "password" : "' + userPassword + '"}',
//                 beforeSend: function (xhr){xhr.setRequestHeader('Authorization', "Basic " + auth); 
// },                  success: function(response) {
//         //success block
//                 // 
//                 // console.log('response => ', response)
//                 // 
//                 window.location = "./prof.html"; 

//               },
//               error: function (xhr, ajaxOptions, thrownError) {
//                   console.log(xhr.status);
//                   console.log(thrownError);
//                 }
// });
        

    //  // Submit form with id function.
    //  function submit_by_id() {
    //     var email = document.getElementById("email").value;
    //     console.log(email);
    //     var password = document.getElementById("password").value;

    //     if (validation()) // Calling validation function
    //     {
    //    
    //     }
    //     }
    // function validation() {
    //     var password = document.getElementById("password").value;
    //     var email = document.getElementById("email").value;
    //     var emailReg = /^([w-.]+@([w-]+.)+[w-]{2,4})?$/;
    //     if (password === '' || email === '') {
    //     alert("Please fill all fields...!!!!!!");
    //     return false;
    //     } else if (!(email).match(emailReg)) {
    //     alert("Invalid Email...!!!!!!");
    //     return false;
    //     } else {
    //     return true;
    //     }
    //     }
