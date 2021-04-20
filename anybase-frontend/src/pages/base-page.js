import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";

import styles from "../components/common/common-styles.module.css";

import { Navigation } from "../components/navigation/navigation";
import { AnytyEditor } from "./anyty-editor";
import { Manyties } from "./manyties";
import { MAnytyDetails } from "./manyty-details";
import { MAnytyEditor } from "./manyty-editor"
import { Users } from "./users";

export function BasePage() {

  return (
    <Router>
      <div>

        <Navigation />

        <div className={styles.mainContainer}>

          <Route exact path="/manyties" component={Manyties} />
          <Route exact path="/manyties/create" component={MAnytyEditor} />
          <Route path="/manyties/:manyty_id/create/" component={AnytyEditor} />
          <Route path="/manyties/:manyty_id/details" component={MAnytyDetails} />
          <Route exact path="/users" component={Users} />

        </div>
      </div>
    </Router>
  );
}
