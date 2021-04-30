import { Button, Grid } from "@material-ui/core";
import React from "react";
import { TitleRowButtons } from "../components/common/title-row";
import { getOneMAnyty } from "../services/meta-anyty/meta-anyty-service";

export class MAnytyDetails extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            metaAnyty: null
        };
    }

    componentDidMount() {
        getOneMAnyty(this.props.match.params.manyty_id).then((mAnyty) => {
            this.setState({
                metaAnyty: mAnyty
            });
        }).catch(r => {
            this.setState({ metaAnyty: null });
            console.error(r);
        })
    }

    render() {
        if (!this.state.metaAnyty) {
            return (
                <span>Loading ...</span>
            );
        }

        return (
            <Grid container direction="column" spacing={2}>
                <Grid item container>
                    <TitleRowButtons buttons={[
                        <Button variant="contained"
                            size="medium"
                            color="secondary"
                            onClick={() => { console.log("DELETE Button pressed.") }}
                        >DELETE</Button>,

                        <Button variant="contained"
                            color="secondary"
                            size="medium"
                            onClick={() => {
                                return this.props.history.push(
                                    `/manyties/${this.state.metaAnyty._manyty_id}/create/`);
                            }}
                        >CREATE</Button>

                    ]} titleText={this.state.metaAnyty.nameRep} />
                </Grid>
            </Grid>
        );
    }
}