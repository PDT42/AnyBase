import React from "react";
import { Button } from "@material-ui/core";

import { TitleRowButton } from "../components/common/title-row";
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
        <TitleRowButton titleText="Meta Anyties" button={
          <Button variant="contained"
            color="secondary"
            size="medium"
            onClick={() => this.props.history.push('/manyties/create')}
          >add</Button>
        } />
        <AnytyList {...this.props} listAnyties={this.state.listAnyties} />
      </div>
    );
  }
}