import React, { Component } from 'react';
import { CONFIG } from './config.js';


import { twitterService } from './utils/twitter.service.js';
export class Dashboard extends Component {
  constructor() {
    super();
    this.state = {
        players: []
    };
  }

  componentDidMount() {
    twitterService.getData()
    .then(result => this.setState({players: result.data}));
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