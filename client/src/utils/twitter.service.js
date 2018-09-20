import { CONFIG } from '../config.js';

const axios = require('axios');

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length === 2) return parts.pop().split(";").shift();
}

export const twitterService = {
    getData() {
        const authCookies = getCookie('Authorization');
        const headers = {
            'Authorization': authCookies ? authCookies : '',
            'Content-Type': 'application/json'
        };
        return axios.get(CONFIG.API_BASE_URL + CONFIG.API_PLAYER_URL, {
            withCredentials: true,
            headers: headers
        });
    }
};