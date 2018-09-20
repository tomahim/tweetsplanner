import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link, Redirect, Switch } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import { Login } from './Login.js';
import { LoggedIn } from './LoggedIn.js';
import { Dashboard } from './Dashboard.js';
import { PrivateRoute } from './PrivateRoute.js';
import { authService } from './utils/auth.service.js';

const Welcome = () => (
    <div>
        <h1>Welcome to the Tweet Planner App !</h1>
        <Login />
    </div>
)

// The Header creates links that can be used to navigate
// between routes.
class Header extends React.Component {

  constructor() {
    super();
    this.state = {
        redirectToLogin: false
    };
    this.logout = this.logout.bind(this);
  }

  logout = () => {
    authService.logout();
    this.setState({redirectToLogin: true});
  }

  render() {
    return (
      <Router>
        <header>
          {this.state.redirectToLogin &&
            <Redirect
              to={{
                pathname: "/"
              }}
            />
          }
          <ul>
            <li>
              <Link to="/dashboard">Dashboard</Link>
              &nbsp;<a onClick={this.logout}>Logout</a>
            </li>
          </ul>

          <hr />
          <Switch>
              <Route exact path="/" component={Welcome} />
              <Route exact path="/loggedin" component={LoggedIn} />
              <PrivateRoute exact path="/dashboard" component={Dashboard} />
          </Switch>
        </header>
      </Router>
    );
  }
}

class App extends Component {
  render() {
    return (
      <div>
          <Header />
      </div>
    );
  }
}

export default App;