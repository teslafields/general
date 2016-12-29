import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import Sidebar from './Components/Sidebar';
import {Router, Route, IndexRoute, hashHistory} from 'react-router';
import './index.css';

ReactDOM.render(
  <Router history={hashHistory}>
    <Route path="/" component={App}>
      <IndexRoute component={App}></IndexRoute>
      <Route path="bars" component={Sidebar}></Route>
    </Route>
  </Router>,
  document.getElementById('root')
);
