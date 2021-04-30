import { Button, Grid } from "@material-ui/core";
import React from "react";
import { TotalAnyties } from "../components/layout-components/total-anyties";
import { TitleRowButtons } from "../components/title-row";
import { getAllAnyties } from "../services/anyty-service";
import { getOneMAnyty } from "../services/meta-anyty-service";
import { Anyty } from "../types/Anyty";
import { MetaAnyty } from "../types/MetaAnyty";

interface MAnytyDetailsProps {
    match: any;
    history: any;
}

interface MAnytyDetailsState {
    metaAnyty?: MetaAnyty;
    anyties: Anyty[]
}

export class MAnytyDetails extends React.Component<MAnytyDetailsProps, MAnytyDetailsState> {

    constructor(props: MAnytyDetailsProps) {
        super(props);

        this.state = {
            metaAnyty: undefined,
            anyties: []
        };
    }

    componentDidMount() {
        getOneMAnyty(this.props.match.params.manyty_id).then((mAnyty: MetaAnyty) => {

            getAllAnyties(mAnyty._manyty_id!).then((anyties: Anyty[]) => {
                
                this.setState({
                    metaAnyty: mAnyty,
                    anyties: anyties
                });

            });
        }).catch(r => {
            this.setState({ metaAnyty: undefined });
            console.error(r);
        })
    }

    render() {
        if (this.state.metaAnyty === undefined) {
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
                                    `/manyties/${this.state.metaAnyty!._manyty_id}/create/`);
                            }}
                        >CREATE</Button>

                    ]} titleText={this.state.metaAnyty.nameRep} />
                </Grid>
                <TotalAnyties totalAnyties={this.state.anyties.length}/>
            </Grid>
        );

    }
}