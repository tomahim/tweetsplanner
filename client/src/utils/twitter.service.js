import { CONFIG } from '../config.js';

const axios = require('axios');

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function getAuthHeaders() {
    const authCookies = getCookie('Authorization');
    return {
        'Authorization': authCookies ? authCookies : ''
    };
}

export const twitterService = {
    get() {
        return axios.get(CONFIG.API_BASE_URL + CONFIG.API_TWEET_URL, {
            withCredentials: true,
            headers: getAuthHeaders()
        }).then(response => {
            return response.data.map(el => {
                return {
                    ...el,
                    send_date: new Date(el.send_date).toLocaleString()
                };
            });
        });
    },
    add(text, date) {
        return axios.post(CONFIG.API_BASE_URL + CONFIG.API_TWEET_URL, {text, date}, {
            withCredentials: true,
            headers: getAuthHeaders()
        });
    },
    remove(id) {
        return axios.delete(CONFIG.API_BASE_URL + CONFIG.API_TWEET_URL + '/' + id, {
            withCredentials: true,
            headers: getAuthHeaders()
        });
    },
    update(id, text) {
        return axios.put(CONFIG.API_BASE_URL + CONFIG.API_TWEET_URL + '/' + id, {text}, {
            withCredentials: true,
            headers: getAuthHeaders()
        });
    }
};