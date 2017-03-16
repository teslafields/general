import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import Students from './Pages/Students'
import Schools from './Pages/Schools'
import Teachers from './Pages/Teachers'
import Home from './Pages/Home'
import Layout from './Pages/Layout'
import { Router, Route, IndexRoute, hashHistory } from "react-router";


ReactDOM.render(
  <Router history={hashHistory}>
    <Route path="/" component={Layout}>
      <Route path="home" name="home'" component={Home}></Route>
      <Route path="students" name="students" component={Students}></Route>
      <Route path="teachers" name="teachers" component={Teachers}></Route>
      <Route path="schools" name="schools" component={Schools}></Route>
    </Route>
  </Router>,
  document.getElementById('root')
);
