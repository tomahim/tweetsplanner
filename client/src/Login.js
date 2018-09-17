import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';

import { authService } from './utils/auth.js';


export class Login extends Component {
  constructor() {
      super();
      this.state = {
        redirectToReferrer: false
      };
  }

  login = () => {
    authService.authenticate('tom', 'toto')
     .then(() => {
        this.setState({ redirectToReferrer: true });
     });
  };

  shouldComponentUpdate(nextProps, nextState) {
    return true;
  }

  render() {
    const { from } = this.props.location.state || { from: { pathname: "/" } };
    const { redirectToReferrer } = this.state;

    console.log('qdkjfskdfjlsdkjf')
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