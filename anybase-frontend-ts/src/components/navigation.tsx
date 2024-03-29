import React from "react";
import { NavLink } from "react-router-dom";

import navStyles from "./navigation.module.css";

export class Navigation extends React.Component {

  render() {
    return (
      <nav>
        <div className={navStyles.navBar}>
          <NavLink
            to="/manyties"
            className={navStyles.navText}
            activeClassName={navStyles.navTextActive}
          >
            MAnyties
          </NavLink>

          <NavLink
            to="/users"
            className={navStyles.navText}
            activeClassName={navStyles.navTextActive}
          >
            Users
          </NavLink>
        </div>
      </nav>
    );
  }
}