import React from "react";
import { Box, Button, Grid, Paper, TextField } from "@material-ui/core";

import { TitleRowButtons } from "../components/common/title-row";
import { HDivider } from "../components/common/common-components";
import { getAllMAnyties } from "../services/meta-anyty/meta-anyty-service";

export class AnytyEditor extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            metaAnytyId: Number(this.props.match.params.manyty_id),
            metaAnyty: null,
            metaAnytyInitialized: false,
            metaAnyties: [],
            anybuteValues: {},
            anylationValue: {}
        }
    }

    componentDidMount() {

        getAllMAnyties().then((mAnyties) => {
            const foundMAnyties = mAnyties.filter(mAnyty => {
                return mAnyty._manyty_id === this.state.metaAnytyId;
            });

            if (foundMAnyties.length > 0) {

                const mAnyty = foundMAnyties[0];

                // Init mappings that will hold
                // all required parameters
                let anybuteValues = {};
                mAnyty.anybutes.map(anybute => {
                    anybuteValues[anybute.columnName] = '';
                    return anybute;
                });
                let anylationValues = {};
                mAnyty.anylations.map(anylation => {
                    anylationValues[anylation.columnName] = '';
                    return anylation;
                });

                // Update State
                this.setState({
                    metaAnyties: mAnyties,
                    metaAnyty: mAnyty,
                    metaAnytyInitialized: true,
                    anybuteValues: anybuteValues,
                    anylationValues: anylationValues
                });
            } else {
                this.setState({
                    metaAnyties: mAnyties,
                    metaAnyty: null,
                    metaAnytyInitialized: true
                });
            }

        }).catch(r => {
            this.setState({
                metaAnyties: [],
                metaAnytyInitialized: true
            });
            console.error(r)
        });
    }

    // Define an onChange function for the anybute inputs
    onAnybuteValueChanged = (event, anybute) => {
        let anylationValues = this.state.anybuteValues;
        anylationValues[anybute.columnName] = event.target.value;
        this.setState({ anylationValues: anylationValues });
    }

    // Define an onChange function for the anylation inputs
    onAnylationValueChanged = (event) => {

    }

    // Define a function to store the specified Anyty
    onSaveButtonClicked = (event) => {
        console.log("Save Button clicked!")
    }

    render() {
        // If data is not yet available ...
        if (!this.state.metaAnytyInitialized) {
            return (<div>Loading ...</div>)
        }

        // If getting data failed ... 
        if (!this.state.metaAnyty) {
            return (<div>Meta Anyty could not be found!</div>)
        }

        // Go for it!
        return (
            <Grid container direction="column" spacing={2}>
                <Grid item container>
                    <TitleRowButtons buttons={[
                        <Button variant="contained"
                            color="secondary"
                            size="medium"
                            onClick={this.onSaveButtonClicked}
                        >Save</Button>
                    ]} titleText={`Create Anyty: ${this.state.metaAnyty.nameRep}`}
                    />
                </Grid>

                <Grid item>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <Form formTitle={'Anybutes'}
                                formRows={this.state.metaAnyty.anybutes.map((anybute, index) => {
                                    return (
                                        <AnybuteFormRow
                                            key={index}
                                            anybute={anybute}
                                            anybuteValue={this.state.anybuteValues[anybute.columnName]}
                                            anybuteIndex={index}
                                            onChange={this.onAnybuteValueChanged}
                                        />
                                    );
                                })} />
                        </Grid>
                        <Grid item xs={12}>
                            <Form formTitle={'Anylations'}
                                formRows={this.state.metaAnyty.anylations.map((anylation, index) => {
                                    return (
                                        <AnylationFormRow
                                            key={index}
                                            anylation={anylation}
                                            anylationValue={this.state.anylationValue[anylation.columnName]}
                                            anylationIndex={index}
                                            onChange={this.onAnylationValueChanged}
                                        />
                                    );
                                })} />
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        );
    }
}

class Form extends React.Component {
    render() {
        return (
            <Paper>
                <Box p={1}>
                    <Grid container direction="column" spacing={1}>
                        <FormHeader title={this.props.formTitle} />
                        <Grid item xs={12}>
                            <HDivider />
                        </Grid>

                        {/* Display Form Rows */}
                        {this.props.formRows}

                    </Grid>
                </Box>
            </Paper>
        );
    }
}

class FormHeader extends React.Component {
    render() {
        return (
            <Grid item container direction="row" xs={12}>
                <Grid item xs={12}>
                    <span>{this.props.title}</span>
                </Grid>
            </Grid>
        );
    }
}

class AnybuteFormRow extends React.Component {
    render() {
        return (
            <Grid item xs={12} key={this.props.anybuteIndex} container direction="row">
                <Grid item xs={12}>
                    <TextField
                        id={this.props.anybute.columnName}
                        size="small"
                        fullWidth
                        label={this.props.anybute.nameRep}
                        value={this.props.anybuteValue}
                        onChange={(event) => this.props.onChange(event, this.props.anybute)}
                    />
                </Grid>
            </Grid>
        );
    }
}

class AnylationFormRow extends React.Component {
    render() {
        return (
            <Grid item xs={12} key={this.props.anylationIndex} container direction="row">
                <Grid item xs={4}>
                    <span>xxx</span>
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