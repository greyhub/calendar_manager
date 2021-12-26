import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import Login from './components/Login';
import Activities from './components/Activities';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="container">
        <Route exact path="/" component={Login} />
        <Route path="/activities" component={Activities} />
      </div>
    );
  }
}

export default App;
