function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

// This sign-in funciont and the code are provided by Google
function onSignIn(googleUser) {
    profile = googleUser.getBasicProfile();
    console.log('Logged in as: ' + googleUser.getBasicProfile().getName());
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    var id_token = googleUser.getAuthResponse().id_token;
    console.log('ID Token: ' + id_token);

    // Create cookie to remember user by their id number and name
    setCookie("id_number", profile.getId(), 1);
    setCookie("user_name", profile.getName(), 1);
    
    //Testing cookie
    var x = document.cookie;
    console.log(x);
    
    /* Code for verifying ID tokens, security is not critical so not implemented yet
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://cs160testingaaa.000webhostapp.com/LogIn.html');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        console.log('Signed in as: ' + xhr.responseText);
    };
    xhr.send('idtoken=' + id_token);
    */
}

function onSuccess(googleUser) {
    console.log('Logged in as: ' + googleUser.getBasicProfile().getName());
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

function getUserID() {
    if(document.cookie.indexOf('id_number=') === -1){
        return "defaultId";
    }
    else{
        return profile.getId();
    }
}

function drop() {
    document.getElementById("dropdown").classList.toggle("show");
}

window.onclick = function(e) {
    if (!e.target.matches('.drop a')) {
        var dropdown = document.getElementById("dropdown");
        if (dropdown.classList.contains('show'))
        { dropdown.classList.remove('show'); }
    }
}

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        //Delete the cookie
        document.cookie = "id_number=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        document.cookie = "user_name=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        console.log('User signed out.');
        location.reload();
    });
}

function validateLogin(){
    if(profile === null){
        alert("You need to log in first!");
    }
}
