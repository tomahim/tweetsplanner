import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';

import { authService } from './utils/auth.js';

export class Login extends Component {
  constructor() {
    super();
    this.state = {
        username: '',
        password: '',
        error: false,
        redirectToReferrer: false
    };

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleSubmit(event) {
    authService.authenticate(
        this.state.username,
        this.state.password
    )
    .then(response => {
        this.setState({redirectToReferrer: true});
     })
     .catch(() => {
        this.setState({error: true});
     });
     event.preventDefault();
  }

  handleChange(e) {
    const {name, value} = e.target;
    this.setState({
      [name]: value
    });
  }

  render() {
    const { from } = this.props.location.state || { from: { pathname: "/" } };
    const { redirectToReferrer } = this.state;

    if (redirectToReferrer) {
      return <Redirect to={from} />;
    }

    return (
      <div>
          <h1>Login</h1>
          {this.state.error && (<div>Error</div>)}
          <div>
            <p>You must log in to view the page at {from.pathname}</p>
            <form onSubmit={this.handleSubmit}>
              <label>
                Username:
                <input value={this.state.username} type="text" name="username" onChange={this.handleChange} />
              </label>
              <label>
                Password:
                <input value={this.state.password} type="password" name="password" onChange={this.handleChange}  />
              </label>
              <input type="submit" value="Submit"/>
            </form>
          </div>
       </div>
    );
  }
}