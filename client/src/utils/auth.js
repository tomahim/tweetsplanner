import { CONFIG } from '../config.js';

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
        body: JSON.stringify({
            username,
            password
        })
      })
      .then(response => response.json())
      .then(response => {
        document.cookie = response.cookie;
      });
  },
  signout(cb) {
    // TODO
  }
};