import './App.css';
import { Switch, Route } from "react-router-dom";
import Layout from "./components/Layout/Layout";
import React, { Fragment } from 'react';

const HomePage = React.lazy(() => import("./pages/HomePage"));

function App() {
  return (
    <Fragment>
      <div>
        <Layout/>
        <Switch>
            <Route exact path="/">
              <HomePage />
            </Route>
        </Switch>
      </div>
    </Fragment>
  );
}

export default App;
