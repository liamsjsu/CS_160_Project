// Global variable for profile
var profile = null;

// This sign-in funciont and the code are provided by Google
function onSignIn(googleUser) {
    profile = googleUser.getBasicProfile();
    console.log('Logged in as: ' + googleUser.getBasicProfile().getName());
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    var id_token = googleUser.getAuthResponse().id_token;
    console.log('ID Token: ' + id_token);
    
    /*
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://cs160testingaaa.000webhostapp.com/LogIn.html');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        console.log('Signed in as: ' + xhr.responseText);
    };
    xhr.send('idtoken=' + id_token);
    */
}

function onFailure(error) {
    console.log(error);
}

function renderButton() {
    gapi.signin2.render('my-signin2', {
        'scope': 'profile email',
        'width': 240,
        'height': 50,
        'longtitle': true,
        'theme': 'dark',
        'onsuccess': onSuccess,
        'onfailure': onFailure
    });
}

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.');
    });
}

function validateLogin(){
    if(profile === null){
        alert("You need to log in first!");
    }
}

$("#sign").click(function(){
    $("#gsign").click();
});

$("#upload").click(function(){
    $("#newFile").click();
});

$("#alanyze").click(function(){
    analyze();
});

function analyze(){
}