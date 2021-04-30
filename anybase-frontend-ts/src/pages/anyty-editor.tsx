import React from "react";
import { Box, Button, Grid, Paper, TextField } from "@material-ui/core";

import { TitleRowButtons } from "../components/title-row";
import { HDivider } from "../components/common-components";
import { getAllMAnyties } from "../services/meta-anyty-service";
import { MetaAnyty } from "../types/MetaAnyty";
import { Anybute } from "../types/Anybute";
import { Anylation } from "../types/Anylation";
import { createAnyty } from "../services/anyty-service";
import { AnytyDTO } from "../types/Anyty";

interface AnytyEditorProps {
    match: any;
}

interface AnytyEditorState {
    metaAnytyId: number;
    metaAnyty?: MetaAnyty;
    metaAnytyInitialized: boolean;
    metaAnyties: MetaAnyty[];
    anybuteValues: Map<string, any>;
    anylationValues: Map<string, any>;
}

export class AnytyEditor extends React.Component<AnytyEditorProps, AnytyEditorState> {

    constructor(props: AnytyEditorProps) {
        super(props);

        this.state = {
            metaAnytyId: Number(this.props.match.params.manyty_id),
            metaAnyty: undefined,
            metaAnytyInitialized: false,
            metaAnyties: [],
            anybuteValues: new Map(),
            anylationValues: new Map()
        }
    }

    componentDidMount() {

        getAllMAnyties().then((mAnyties: MetaAnyty[]) => {
            const foundMAnyties = mAnyties.filter((mAnyty: MetaAnyty) => {
                return mAnyty._manyty_id === this.state.metaAnytyId;
            });

            if (foundMAnyties.length > 0) {

                const mAnyty: MetaAnyty = foundMAnyties[0];

                // Init Mapping that will hold set Anybute Values
                let anybuteValues: Map<string, any> = new Map();
                mAnyty.anybutes.map((anybute: Anybute) => {
                    if (anybute.editable) {
                        anybuteValues.set(anybute.columnName!, '');
                    }
                    return anybute;
                });

                // Init Mapping that will hold set Anylation Values
                let anylationValues: Map<string, any> = new Map();
                mAnyty.anylations.map((anylation: Anylation) => {
                    if (anylation.editable) {
                        anylationValues.set(anylation.columnName!, '');
                    }
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

                // No Data
                this.setState({
                    metaAnyties: mAnyties,
                    metaAnyty: undefined,
                    metaAnytyInitialized: true
                });
            }
        }).catch(r => {

            // Error
            this.setState({
                metaAnyties: [],
                metaAnytyInitialized: true
            });
            console.error(r)
        });
    }

    // Define an onChange function for the anybute inputs
    onAnybuteValueChanged = (event: any, anybute: Anybute) => {
        let anybuteValues = this.state.anybuteValues;
        anybuteValues.set(anybute.columnName!, event.target.value);
        this.setState({ anylationValues: anybuteValues });
    }

    // Define an onChange function for the anylation inputs
    onAnylationValueChanged = (event: any, anylation: Anylation) => {
        let anylationValues = this.state.anylationValues;
        anylationValues.set(anylation.columnName!, event.target.value);
        this.setState({ anylationValues: anylationValues });
    }

    // Define a function to store the specified Anyty
    onSaveButtonClicked = (event: any) => {

        const anytyDTO: AnytyDTO = {
            mAnytyId: this.state.metaAnytyId,
            anybutes: Array.from(this.state.anybuteValues.entries()),
            anylations: Array.from(this.state.anylationValues.entries())
        };

        createAnyty(anytyDTO);

        console.log("Save Button clicked!");
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
                            <Form formTitle='Anybutes'
                                formRows={this.state.metaAnyty.anybutes.map((anybute, index) => {
                                    return (
                                        <AnybuteFormRow
                                            key={index}
                                            anybute={anybute}
                                            anybuteValue={this.state.anybuteValues.get(anybute.columnName!)}
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
                                            anylationValue={this.state.anylationValues.get(anylation.columnName!)}
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

interface FormProps {
    formTitle: string
    formRows: JSX.Element[]
}

class Form extends React.Component<FormProps, any> {
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

interface FormHeaderProps {
    title: string
}

class FormHeader extends React.Component<FormHeaderProps, any> {
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

interface AnybuteFormRowProps {
    anybuteIndex: number;
    anybute: Anybute;
    anybuteValue: any;
    onChange: any;
}

class AnybuteFormRow extends React.Component<AnybuteFormRowProps, any> {
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

interface AnylationFormRowProps {
    anylationIndex: number;
    anylation: Anylation;
    anylationValue: any;
    onChange: any;
}

class AnylationFormRow extends React.Component<AnylationFormRowProps, any> {
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