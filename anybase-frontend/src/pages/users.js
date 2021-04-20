import React from "react";

import { TitleRow } from "../components/common/title-row";


export class Users extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <div>
        <TitleRow titleText="Users" />
      </div>
    );
  }
}
