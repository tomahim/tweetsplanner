import React, { Component } from 'react';
import { CONFIG } from './config.js';


import { twitterService } from './utils/twitter.service.js';

Date.prototype.toIsoString = function() {
    var tzo = -this.getTimezoneOffset(),
        dif = tzo >= 0 ? '+' : '-',
        pad = function(num) {
            var norm = Math.floor(Math.abs(num));
            return (norm < 10 ? '0' : '') + norm;
        };
    return this.getFullYear() +
        '-' + pad(this.getMonth() + 1) +
        '-' + pad(this.getDate()) +
        'T' + pad(this.getHours()) +
        ':' + pad(this.getMinutes()) +
        ':' + pad(this.getSeconds()) +
        dif + pad(tzo / 60) +
        ':' + pad(tzo % 60);
}

export class Dashboard extends Component {
  constructor() {
    super();
    this.state = {
        tweets: []
    };
  }

  componentDidMount() {
    twitterService.get()
    .then(result => this.setState({tweets: result.data}));
  }

  addTweet(text) {
    twitterService.add(text, new Date().toIsoString()).then(result => {
        this.setState({
            tweets: this.state.tweets.concat({id: result.data.id, text: text, status: 'DRAFT'})
        });
    });
  }

  editTweet(id, text) {
    twitterService.update(id, text).then(() => {
        this.setState({
            tweets: this.state.tweets.map(item => {
                if (item.id !== id) {
                    return item;
                }
                return {
                    ...item,
                    text: text
                };
            })
        });
    });
  }

  removeTweet(id) {
    twitterService.remove(id).then(() => {
        this.setState({tweets: this.state.tweets.filter(tweet => tweet.id !== id)});
    });
  }

  render() {
    const tweets = this.state.tweets.map((tweet, index) => {
        return (
            <li key={index}>
                {tweet.id} - {tweet.text} - {tweet.status}
                <button onClick={()=>this.editTweet(tweet.id, 'edited tweet !')}>Edit</button>
                <button onClick={()=>this.removeTweet(tweet.id)}>Delete</button>
            </li>
        );
    });

    return (
      <div>
          <h1>Tweets list</h1>
          <ul>
            {tweets}
          </ul>
          <button onClick={()=>this.addTweet('Meilleur tweet')}>Add</button>
      </div>
    );
  }
}