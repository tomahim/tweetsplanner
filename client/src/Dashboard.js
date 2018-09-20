import React, { Component } from 'react';
import { CONFIG } from './config.js';


import { twitterService } from './utils/twitter.service.js';
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

  removeTweet(id) {
    twitterService.remove(id).then(() => {
        this.setState({tweets: this.state.tweets.filter(tweet => tweet.id !== id)});
    });
  }

  addTweet(text) {
    twitterService.add(text).then((result) => {
        this.setState({
            tweets: this.state.tweets.concat({id: result.data.id, text: text, status: 'DRAFT'})
        });
    });
  }

  render() {
    const tweets = this.state.tweets.map((tweet, index) => {
        return (
            <li key={index}>
                {tweet.id} - {tweet.text} - {tweet.status}
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