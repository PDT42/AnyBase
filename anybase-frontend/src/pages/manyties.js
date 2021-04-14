import React from "react";

import { TitleRowAddButton } from "../components/common/title-row";
import { AnytyList } from "../components/item-list/item-list";
import { getAllMAnyties } from "../services/meta-anyty/meta-anyty-service";

export class Manyties extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      listAnyties: []
    };
  }

  componentDidMount() {
    getAllMAnyties().then((mAnyties) => {
      this.setState({ listAnyties: mAnyties })
    }).catch(r => {
      console.log(r);
      this.setState({ listAnyties: [] });
    });
  }

  render() {
    return (
      <div>
        <TitleRowAddButton {...this.props} titleText="Meta Anyties"/>
        <AnytyList {...this.props} listAnyties={this.state.listAnyties} />
      </div>
    );
  }
}