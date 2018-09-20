import { CONFIG } from '../config.js';

const axios = require('axios');

function deleteCookie(cname) {
    var d = new Date(); //Create an date object
    d.setTime(d.getTime() - (1000*60*60*24)); //Set the time to the past. 1000 milliseonds = 1 second
    var expires = "expires=" + d.toGMTString(); //Compose the expirartion date
    window.document.cookie = cname + "=" + "; " +expires;//Set the cookie with name and the expiration date
}

export const authService = {
  isAuthenticated() {
      return document.cookie.split('Authorization=') && document.cookie.split('Authorization=').length === 2;
  },
  authenticate() {
      return axios.post(
        CONFIG.API_BASE_URL + CONFIG.API_USER_URL + '/login',
        {},
        {withCredentials: true}
      )
      .then(response => {
        if (response.status !== 200) {
            return Promise.reject();
        }
        document.location = response.data.authenticate_url;
      });
  },
  confirmAuthenticate(oauthToken, oauthVerifier) {
    const headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    };
    return axios.post(
        CONFIG.API_BASE_URL + CONFIG.API_USER_URL + '/confirm_authenticate',
        {oauth_token: oauthToken, oauth_verifier: oauthVerifier},
        {withCredentials: true}
      );
  },
  logout(cb) {
    deleteCookie('Authorization');
  }
};