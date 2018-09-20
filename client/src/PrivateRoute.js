import React, { Component } from 'react';
import { Route, Redirect } from 'react-router-dom';
import { authService } from './utils/auth.js';
import { CONFIG } from './config.js';

export const PrivateRoute = ({ component: Component, ...rest }) => (
  <Route
    {...rest}
    render={props =>
      authService.isAuthenticated() ? (
        <Component {...props} />
      ) : (
        <Redirect
          to={{
            pathname: "/",
            state: { from: props.location }
          }}
        />
      )
    }
  />
);