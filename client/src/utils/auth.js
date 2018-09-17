import { CONFIG } from '../config.js';

function deleteCookie(cname) {
    var d = new Date(); //Create an date object
    d.setTime(d.getTime() - (1000*60*60*24)); //Set the time to the past. 1000 milliseonds = 1 second
    var expires = "expires=" + d.toGMTString(); //Compose the expirartion date
    window.document.cookie = cname+"="+"; "+expires;//Set the cookie with name and the expiration date

}

export const authService = {
  isAuthenticated() {
      return document.cookie.split('Authorization=') && document.cookie.split('Authorization=').length === 2;
  },
  authenticate(username, password) {
      return fetch(CONFIG.API_BASE_URL + CONFIG.API_USER_URL + '/login', {
        method: 'post',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({username, password})
      })
      .then(response => {
        if (response.status !== 200) {
            return Promise.reject();
        }
        return response.json();
      })
      .then(response => {
        document.cookie = response.cookie;
      });
  },
  logout(cb) {
    deleteCookie('Authorization');
  }
};