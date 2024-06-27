// assets/js/auth.js

document.addEventListener("DOMContentLoaded", function() {
  var webAuth = new auth0.WebAuth({
    domain: 'dev-qvewjycxd7q0rel6.eu.auth0.com',
    clientID: '7zBqayaQF1g8W7Bj3efl9JidwNmFonUQ',
    redirectUri: window.location.href,
    responseType: 'token id_token',
    scope: 'openid profile email'
  });

  function login() {
    webAuth.authorize();
  }

  function handleAuthentication() {
    webAuth.parseHash(function(err, authResult) {
      if (authResult && authResult.accessToken && authResult.idToken) {
        window.location.hash = '';
        setSession(authResult);
      } else if (err) {
        console.log(err);
        alert('Error: ' + err.error + '. Check the console for further details.');
      }
    });
  }

  function setSession(authResult) {
    var expiresAt = JSON.stringify(authResult.expiresIn * 1000 + new Date().getTime());
    localStorage.setItem('access_token', authResult.accessToken);
    localStorage.setItem('id_token', authResult.idToken);
    localStorage.setItem('expires_at', expiresAt);
  }

  function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('id_token');
    localStorage.removeItem('expires_at');
    webAuth.logout({ returnTo: window.location.origin });
  }

  function isAuthenticated() {
    var expiresAt = JSON.parse(localStorage.getItem('expires_at'));
    return new Date().getTime() < expiresAt;
  }

  if (window.location.hash) {
    handleAuthentication();
  }

  if (!isAuthenticated()) {
    login();
  }

  document.querySelector("#login").addEventListener("click", login);
  document.querySelector("#logout").addEventListener("click", logout);
});