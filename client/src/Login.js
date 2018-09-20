import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';

import { authService } from './utils/auth.service.js';
import PropTypes from 'prop-types'

import { withRouter } from 'react-router'

class LoginCmp extends Component {
  static propTypes = {
    match: PropTypes.object.isRequired,
    location: PropTypes.object.isRequired,
    history: PropTypes.object.isRequired
  }

  state = {
    error: false,
    redirectToReferrer: false
  };

  login(event) {
    authService.authenticate()
    .then(response => {
        this.setState({redirectToReferrer: true});
     })
     .catch(() => {
        this.setState({error: true});
     });
     event.preventDefault();
  }

  render() {
    const { from } = this.props.location.state || { from: { pathname: "/" } };
    const { redirectToReferrer } = this.state;

    if (redirectToReferrer) {
        return <Redirect to={from} />;
    }
    return (
        <div>
            <h3>Login</h3>
            {this.state.error && (<div>Error</div>)}
            <button onClick={this.login.bind(this)}>Log in with Twitter</button>
        </div>
    );
  }
}

export const Login = withRouter(LoginCmp)