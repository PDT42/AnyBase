import React from "react";
import { Box, Button, Grid, Paper, TextField } from "@material-ui/core";

import { TitleRowButton } from "../components/common/title-row";
import { HDivider } from "../components/common/common-components";
import { getAllMAnyties, getOneMAnyty } from "../services/meta-anyty/meta-anyty-service";

export class AnytyEditor extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            metaAnytyId: Number(this.props.match.params.manyty_id),
            metaAnyty: null,
            metaAnyties: [],
            anybuteValues: [],
            anylationValue: []
        }
    }

    componentDidMount() {
        getOneMAnyty(this.state.metaAnytyId).then((mAnyty) => {
            this.setState({ metaAnyty: mAnyty });
        }).catch(r => {
            console.error(r);
        });
        getAllMAnyties().then((mAnyties) => {
            this.setState({ metaAnyties: mAnyties });
        }).catch(r => {
            this.setState({ metaAnyties: [] });
            console.error(r)
        });
    }

    render() {
        if (this.state.metaAnyty == null) {
            return (<div>Loading ...</div>)
        }


        return (
            <div>
                <TitleRowButton button={
                    <Button variant="contained"
                        color="secondary"
                        size="medium"
                        onClick={() => console.log('Save Button Clicked')}
                    >Save</Button>}
                    titleText={`Create Anyty: ${this.state.metaAnyty.nameRep}`}
                />

                <Box marginTop={2}>
                    <Grid container spacing={2}>
                        {this.AnybuteForm()}
                        {this.AnylationForm()}
                    </Grid>
                </Box>
            </div>
        );
    }

    AnybuteForm() {
        const anybuteFormRows = this.state.metaAnyty.anybutes.map((anybute) => {
            if (!anybute.columnName.startsWith('_anyty')) {
                return this.AnybuteFormRow(anybute);
            } else return null;
        }).filter(a => a);

        return (
            <Grid item xs={12}>
                <Paper>
                    <Box p={1}>
                        <Grid container direction="column" spacing={1}>
                            {this.AnybuteFormHeader()}
                            <Grid item xs={12}>
                                <HDivider />
                            </Grid>
                            {anybuteFormRows}
                        </Grid>
                    </Box>
                </Paper>
            </Grid >
        );
    }

    AnybuteFormHeader() {
        return (
            <Grid item container direction="row" xs={12}>
                <Grid item xs={12}>
                    <span>Anybutes</span>
                </Grid>
            </Grid>
        );
    }

    AnybuteFormRow(anybute) {
        return (
            <Grid key={anybute.columnName} item container direction="row" xs={12}>
                <Grid item xs={12}>
                    <TextField
                        id={anybute.columnName}
                        size="small"
                        fullWidth
                        label={anybute.nameRep}
                        value={anybute.nameRep}
                        onChange={(event) => {

                        }}
                    />
                </Grid>
            </Grid>
        );
    }

    AnylationForm() {
        const anylationFormRows = this.state.metaAnyty.anylations.map((anylation) => {
            return this.AnylationFormRow(anylation);
        });

        return (
            <Grid item xs={12}>
                <Paper>
                    <Box p={1}>
                        <Grid container direction="column" spacing={1}>
                            {this.AnylationFormHeader()}
                            <Grid item xs={12}>
                                <HDivider />
                            </Grid>
                            {anylationFormRows}
                        </Grid>
                    </Box>
                </Paper>
            </Grid>
        );
    }

    AnylationFormHeader() {
        return (
            <Grid item container direction="row" xs={12}>
                <Grid item xs={12}>
                    <span>Anylations</span>
                </Grid>
            </Grid>
        );
    }

    AnylationFormRow(anylation) {
        return (
            <Grid key={anylation.columnName} item container direction="row" xs={12}>
                <Grid item xs={4}>
                    <span>Anylation Name Rep</span>
                </Grid>
                <Grid item xs={3}>
                    <span>xxx</span>
                </Grid>
                <Grid item xs={5}>
                    <span>xxx</span>
                </Grid>
            </Grid>
        );
    }
}