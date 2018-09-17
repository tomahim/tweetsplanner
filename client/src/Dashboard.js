import React, { Component } from 'react';
import { CONFIG } from './config.js';

export class Dashboard extends Component {
  constructor() {
    super();
    this.state = {
        players: []
    };
  }

  componentDidMount() {
    const authCookies = document.cookie.split('Authorization=');
    const headers = {
        'Authorization': authCookies && authCookies.length === 2 ? authCookies[1] : '',
        'Content-Type': 'application/json'
    };
    fetch(CONFIG.API_BASE_URL + CONFIG.API_PLAYER_URL, {
        method: 'GET',
        headers: headers
    })
    .then(results => results.json())
    .then(players => this.setState({players: players}));
  }

  render() {
    const players = this.state.players.map((player, index) => <li key={index}>{player.lastname} {player.firstname}</li>);

    return (
      <div>
          <h1>Players list</h1>
          <ul>
            {players}
          </ul>
      </div>
    );
  }
}