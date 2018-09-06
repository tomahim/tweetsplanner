import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';

import { fakeAuth } from './utils/auth.js';


export class Login extends Component {
  constructor() {
      super();
      this.state = {
        redirectToReferrer: false
      };
  }

  login = () => {
    fakeAuth.authenticate(() => {
      this.setState({ redirectToReferrer: true });
    });
  };

  render() {
    const { from } = this.props.location.state || { from: { pathname: "/" } };
    const { redirectToReferrer } = this.state;

    if (redirectToReferrer) {
      return <Redirect to={from} />;
    }

    return (
      <div>
          <h1>Login</h1>
          <div>
            <p>You must log in to view the page at {from.pathname}</p>
            <button onClick={this.login}>Log in</button>
          </div>
       </div>
    );
  }
}