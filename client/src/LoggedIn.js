import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';

import { authService } from './utils/auth.js';



function getParameterByName(name) {
    const url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    const regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

export class LoggedIn extends Component {
  constructor() {
    super();
    this.state = {
        isAuthenticated: false
    };
  }


  componentDidMount() {
    const oauthToken = getParameterByName('oauth_token');
    const oauthVerifier = getParameterByName('oauth_verifier');
    authService.confirmAuthenticate(oauthToken, oauthVerifier).then((response) => {
        console.log('response', response)
        this.setState({isAuthenticated: response.status === 200});
    });
  }

  render() {
    return (<div>{this.state.isAuthenticated &&
            <Redirect
              to={{
                pathname: "/dashboard"
              }}
            />
          }</div>)
  }
}

/*

          {authService.isAuthenticated() &&
            <Redirect
              to={{
                pathname: "/"
              }}
            />
          }
*/