import React from "react";
import { Button, Grid } from "@material-ui/core";

import { TitleRowButtons } from "../components/title-row";
import { getAllMAnyties } from "../services/meta-anyty-service";

import { MetaAnyty } from "../types/MetaAnyty";
import { MAnytyList } from "../components/manyty-list";

interface MAnytiesProps {
    history: any;
}

interface MAnytiesState {
    metaAnyties: MetaAnyty[];
}

export class MAnyties extends React.Component<MAnytiesProps, MAnytiesState> {

    constructor(props: MAnytiesProps) {
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

