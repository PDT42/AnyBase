import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";

import styles from "../components/common-styles.module.css";

import { Navigation } from "../components/navigation";
import { AnytyEditor } from "./anyty-editor";
import { MAnyties } from "./manyties";
import { MAnytyDetails } from "./manyty-details";
import { MAnytyEditor } from "./manyty-editor"
import { Users } from "./users";

export function BasePage() {

  return (
    <Router>
      <div>

        <Navigation />

        <div className={styles.mainContainer}>

          <Route path="/manyties" exact component={MAnyties} />
          <Route path="/manyties/create" exact component={MAnytyEditor} />
          
          <Route path="/manyties/:manyty_id/create/" component={AnytyEditor} />
          <Route path="/manyties/:manyty_id/details" component={MAnytyDetails} />

          <Route path="/users" exact component={Users} />

        </div>
      </div>
    </Router>
  );
}