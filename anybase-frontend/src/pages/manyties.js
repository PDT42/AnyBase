import React from "react";
import { Box, Button, Grid, Paper } from "@material-ui/core";

import { TitleRowButtons } from "../components/common/title-row";
import { getAllMAnyties } from "../services/meta-anyty/meta-anyty-service";

import styles from "../components/common/common-styles.module.css";

export class Manyties extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      metaAnyties: []
    };
  }

  componentDidMount() {

    getAllMAnyties().then((mAnyties) => {
      this.setState({ metaAnyties: mAnyties })
    }).catch(r => {
      console.log(r);
      this.setState({ metaAnyties: [] });
    });
  }

  render() {
    return (
      <Grid container direction="column" spacing={2}>
        <Grid item container>
          <TitleRowButtons titleText="Meta Anyties" buttons={[
            <Button variant="contained"
              color="secondary"
              size="medium"
              onClick={() => this.props.history.push('/manyties/create')}
            >ADD</Button>
          ]} />
        </Grid>

        <Grid item>
          <MAnytyList {...this.props} metaAnyties={this.state.metaAnyties} />
        </Grid>

      </Grid>
    );
  }
}

class MAnytyList extends React.Component {

  onListItemNavigate = (mAnytyId) => {
    this.props.history.push(`/manyties/${mAnytyId}/details`);
  };

  render() {
    if (!this.props.metaAnyties) {
      return (
        <span>Loading ...</span>
      );
    }

    // Create a list item for each of the MAnyties
    const mAnytyList = this.props.metaAnyties.map((mAnyty, index) => {
      return (
        <MAnytyListItem key={mAnyty._manyty_id} mAnyty={mAnyty} mAnytyIndex={index}
          onClick={() => this.onListItemNavigate(mAnyty._manyty_id)}
        />
      );
    });

    return (
      <Grid container direction="column" spacing={2}>
        {mAnytyList}
      </Grid>
    );
  }
}

class MAnytyListItem extends React.Component {
  render() {
    return (
      <Grid item xs={12}>
        <Paper className={styles.paperListItem}>
          <Box p={1} onClick={this.props.onClick}>
            <Grid container direction="column" spacing={1}>
              <Grid item container direction="row" justify="space-between">
                <Grid item>
                  <span>{this.props.mAnyty.nameRep}</span>
                </Grid>
                <Grid item>
                  <span>{this.props.mAnyty._manyty_id}</span>
                </Grid>
              </Grid>
            </Grid>
          </Box>
        </Paper>
      </Grid>
    );
  }
}