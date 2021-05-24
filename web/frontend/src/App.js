import './App.css';
import { Switch, Route } from "react-router-dom";
import Layout from "./components/Layout/Layout";
import React, { Fragment } from 'react';

const HomePage = React.lazy(() => import("./pages/HomePage"));
const DevicesPage = React.lazy(() => import("./pages/DevicesPage"));
const ManageGroupsPage = React.lazy(() => import("./pages/ManageGroupsPage"));
const RegisterDevicePage = React.lazy(() => import("./pages/RegisterDevicePage"));

function App() {
  return (
    <Fragment>
      <div>
        <Layout/>
        <Switch>
            <Route exact path="/">
              <HomePage />
            </Route>
            <Route path="/devices">
              <DevicesPage />
            </Route>
            <Route path="/manage_groups">
              <ManageGroupsPage />
            </Route>
            <Route path="/registerdevice">
              <RegisterDevicePage />
            </Route>
        </Switch>
      </div>
    </Fragment>
  );
}

export default App;
