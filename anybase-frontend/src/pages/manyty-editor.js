import React from "react";
import { Paper, Grid, Checkbox, FormControlLabel, FormGroup, Select, TextField, Button, MenuItem, InputLabel, Box } from "@material-ui/core";
import AddCircleOutlineIcon from '@material-ui/icons/AddCircleOutline';

import { TitleRowButtons } from "../components/common/title-row";
import { HDivider } from "../components/common/common-components";
import { CancelOutlined } from "@material-ui/icons";
import { createMAnyty, getAllMAnyties } from "../services/meta-anyty/meta-anyty-service";

export class MAnytyEditor extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            parentManyties: [],
            selectedParentManyty: '',
            selectedParentAnybutes: 0,
            selectedParentAnylations: 0,
            // --
            _manyty_name: '',
            _manyty_parent_id: 0,
            _manyty_is_property: false,
            _manyty_is_bookable: false,
            _manyty_anybutes: [{
                nameRep: '',
                dataType: 'string',
                required: false
            }],
            _manyty_anylations: [{
                nameRep: '',
                anylationType: 'reference',
                required: false,
                targetMAnytyId: 0,
                anylationMAnytyDTO: {}
            }],
        };

    }

    componentDidMount() {
        getAllMAnyties().then((mAnyties) => {
            this.setState({ parentManyties: mAnyties })
        }).catch(r => {
            this.setState({ parentManyties: [] });
            console.error(r);
        });
    }

    render() {
        const onSaveButtonClicked = () => {
            createMAnyty({
                "nameRep": this.state._manyty_name,
                "parentMAnytyId": this.state.selectedParentManyty._manyty_id || 0,
                "isProperty": this.state._manyty_is_property,
                "isBookable": this.state._manyty_is_bookable,
                "anybutes": this.state._manyty_anybutes,
                "anylations": this.state._manyty_anylations
            }).then(() => {
                this.props.history.push('/manyties')
            });
        }

        return (
            <Grid container direction="column" spacing={2}>
                <Grid item container>
                    <TitleRowButtons buttons={[
                        <Button variant="contained"
                            color="secondary"
                            size="medium"
                            onClick={onSaveButtonClicked}
                        >Save</Button>
                    ]} titleText="Create Meta Anyty" />
                </Grid>

                <Grid item>
                    {this.MAnytyDefaultForm()}
                </Grid>
                <Grid item>
                    <HDivider />
                </Grid>
                <Grid item>
                    {this.MAnytyAnybuteForm()}
                </Grid>
                <Grid item>
                    <HDivider />
                </Grid>
                <Grid item>
                    {this.MAnytyAnylationForm()}
                </Grid>
            </Grid>
        );
    }

    // +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    MAnytyDefaultForm() {
        return (
            <Paper>
                <Box m={1}>
                    <Grid container spacing={2}>

                        {this.MAnytyNameField()}
                        {this.MAnytyParentSelector()}
                        {this.MAnytyBookableCheckbox()}
                        {this.MAnytyPropertyCheckbox()}

                    </Grid>
                </Box>
            </Paper>
        );
    }

    MAnytyNameField() {
        return (
            <Grid item xs={12}>
                <TextField
                    id="name"
                    size="small"
                    fullWidth
                    label="Name"
                    value={this.state._manyty_name}
                    onChange={(event) => {
                        this.setState({ _manyty_name: event.target.value })
                    }}
                />
            </Grid>
        );
    }

    MAnytyParentSelector() {

        // Compile the list of parent options
        const parentManytyOptions = [
            <MenuItem key={0} value={''}>None</MenuItem>,
            ...this.state.parentManyties.map(
                (mAnyty) => this.ParentMAnytyOption(mAnyty))];

        return (
            <Grid item xs={12}>
                <InputLabel shrink id="_manyty_parent_id">
                    Parent Meta Anyty
                </InputLabel>
                <Select
                    id="_manyty_parent_id"
                    size="small"
                    fullWidth
                    label="Parent Meta Anyty"
                    onChange={(event) => {
                        const parent = event.target.value;
                        this.setState({
                            _manyty_parent_id: parent._manyty_id || 0,
                            selectedParentManyty: parent,
                            selectedParentAnybutes: parent.anybutes.length || 0,
                            selectedParentAnylations: parent.anylations.length || 0
                        });
                    }}
                    value={this.state.selectedParentManyty}
                    displayEmpty
                >
                    {parentManytyOptions}
                </Select>
            </Grid>
        );
    }

    ParentMAnytyOption(mAnyty) {
        return (
            <MenuItem key={mAnyty._manyty_id} value={mAnyty}>
                {mAnyty.nameRep}
            </MenuItem>
        );
    }

    MAnytyBookableCheckbox() {
        return (
            <Grid item xs={4}>
                <FormControlLabel control={
                    <Checkbox name="bookable"
                        checked={this.state._manyty_is_bookable}
                        onChange={() => {
                            if (this.state._manyty_is_bookable) {
                                this.setState({
                                    _manyty_is_bookable: false
                                });
                            } else {
                                this.setState({
                                    _manyty_is_bookable: true
                                });
                            }
                        }}
                    />
                } label="Anyties of this type are bookable" />
            </Grid>
        );
    }

    MAnytyPropertyCheckbox() {
        return (
            <Grid item xs={4}>
                <FormControlLabel control={
                    <Checkbox name="property"
                        checked={this.state._manyty_is_property}
                        onChange={() => {
                            if (this.state._manyty_is_property) {
                                this.setState({
                                    _manyty_is_property: false
                                });
                            } else {
                                this.setState({
                                    _manyty_is_property: true
                                });
                            }
                        }}
                    />
                } label="is Property of another Anyty" />
            </Grid>
        );
    }

    // +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    MAnytyAnybuteForm() {

        // Create a disabled Anybute Column for 
        // each Anybute of the selected parent
        let parentAnybuteColumns = [];
        if (this.state.selectedParentManyty) {
            const parentAnybutes = Array.from(this.state.selectedParentManyty.anybutes);
            parentAnybuteColumns = parentAnybutes.map((anybute, index) => {
                return this.AnybuteColumn(anybute, index, true)
            });
        }

        // Create Anybute Columns for 
        // each Anybute already added
        const anybuteColumns = this.state._manyty_anybutes.map((anybuteDTO, index) => {
            let key = index + parentAnybuteColumns.length;
            return this.AnybuteColumn(anybuteDTO, key);
        });

        // Define a function to add a new Anybute
        let addAnybute = () => {
            let currentAnybutes = this.state._manyty_anybutes;

            currentAnybutes.push({
                nameRep: '',
                dataType: 'string',
                required: false
            });
            this.setState({ _manyty_anybutes: currentAnybutes })
        }

        // Define OnClick Handler
        let onAddButtonClick = () => {
            addAnybute();
        }

        return (
            <FormGroup>
                <Paper>
                    <Box p={1}>
                        <Grid container direction="column">
                            {parentAnybuteColumns}
                            {anybuteColumns}
                        </Grid>
                        <Grid item xs={12}>
                            <Box paddingTop={2}>
                                <Button fullWidth
                                    variant="contained"
                                    color="primary"
                                    size="small"
                                    onClick={onAddButtonClick}
                                >
                                    <AddCircleOutlineIcon />
                                </Button>
                            </Box>
                        </Grid>
                    </Box>
                </Paper>
            </FormGroup>
        );
    }

    AnybuteColumn(anybuteDTO, key, disabled = false) {
        return (
            <Grid item xs={12} key={`anybute_${key}`} container direction="row" spacing={2}>

                {this.AnybuteRemoveButton(key, disabled)}
                {this.AnybuteNameField(anybuteDTO.nameRep, key, disabled)}
                {this.AnybuteDataTypeSelector(anybuteDTO.dataType, key, disabled)}
                {this.AnybuteRequiredCheckbox(anybuteDTO.required, key, disabled)}

            </Grid>
        );
    }

    AnybuteRemoveButton(key, disabled) {
        return (
            <Grid item xs={1} container justify="center" alignContent="center">
                <Button
                    id={`_remove_anybute_${key}`}
                    disabled={disabled}
                    onClick={() => {
                        let anybutes = this.state._manyty_anybutes;
                        anybutes.pop(key)

                        this.setState({
                            _manyty_anybutes: anybutes
                        });
                    }}
                >
                    <CancelOutlined />
                </Button>
            </Grid>
        );
    }

    AnybuteNameField(anybuteName, key, disabled) {
        return (
            <Grid item xs={7}>
                <TextField
                    id={`_anybute_column_name_${key}`}
                    size="small" fullWidth
                    label="Anybute Name"
                    disabled={disabled}
                    value={anybuteName}
                    onChange={(event) => {
                        const anybutes = this.state._manyty_anybutes;
                        anybutes[key - this.state.selectedParentAnybutes].nameRep = event.target.value;

                        this.setState({
                            _manyty_anybutes: anybutes
                        })
                    }}
                />
            </Grid>
        );
    }

    AnybuteDataTypeSelector(dataType, key, disabled) {
        return (
            <Grid item xs={3}>
                <InputLabel shrink >
                    DataType
                </InputLabel>
                <Select
                    id={`_anybute_data_type_${key}`}
                    size="small" fullWidth
                    displayEmpty
                    disabled={disabled}
                    value={dataType}
                    onChange={(event) => {
                        let anybutes = this.state._manyty_anybutes;
                        anybutes[key - this.state.selectedParentAnybutes]
                            .dataType = event.target.value;

                        this.setState({
                            _manyty_anybutes: anybutes
                        });
                    }}
                >
                    <MenuItem value={"string"}>String</MenuItem>
                    <MenuItem value={"integer"}>Integer</MenuItem>
                    <MenuItem value={"datetime"}>Datetime</MenuItem>
                </Select>
            </Grid>
        );
    }

    AnybuteRequiredCheckbox(anybuteRequired, key, disabled) {
        return (
            <Grid item xs={1} container justify="flex-end" direction="row">
                <InputLabel shrink>required</InputLabel>
                <Checkbox name="property"
                    id={`_anybute_required_${key}`}
                    checked={anybuteRequired}
                    disabled={disabled}
                    onChange={() => {
                        let anybutes = this.state._manyty_anybutes;
                        if (anybutes[key - this.state.selectedParentAnybutes].required) {
                            anybutes[key - this.state.selectedParentAnybutes].required = false;
                        } else {
                            anybutes[key - this.state.selectedParentAnybutes].required = true;
                        }

                        this.setState({
                            _manyty_anybutes: anybutes
                        });
                    }}
                />
            </Grid>
        );
    }

    // +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    MAnytyAnylationForm() {

        let parentAnylationColumns = [];
        if (this.state.selectedParentManyty) {
            const parentAnylations = Array.from(this.state.selectedParentManyty.anylations);
            parentAnylationColumns = parentAnylations.map((anybute, index) => {
                return this.AnylationColumn(anybute, index, true)
            });
        }

        // Create Anylation Columns for 
        // each Anylation already added
        const anylationColumns = this.state._manyty_anylations.map((anylationDTO, index) => {
            let key = index + parentAnylationColumns.length;
            return this.AnylationColumn(anylationDTO, key);
        });

        // Define a function to add a new Anylation
        let addAnybute = () => {
            let currentAnylations = this.state._manyty_anylations;

            currentAnylations.push({
                nameRep: '',
                anylationType: 'reference',
                required: false,
                targetMAnytyId: 0,
                anylationMAnytyDTO: {}
            });
            this.setState({ _manyty_anylations: currentAnylations })
        }

        // Define OnClick Handler
        let onAddButtonClicked = () => {
            addAnybute();
        }

        return (
            <FormGroup>
                <Paper>
                    <Box p={1}>
                        <Grid container direction="column">
                            {parentAnylationColumns}
                            {anylationColumns}
                        </Grid>
                        <Grid item xs={12}>
                            <Box paddingTop={2}>
                                <Button fullWidth
                                    variant="contained"
                                    color="primary"
                                    size="small"
                                    onClick={onAddButtonClicked}
                                >
                                    <AddCircleOutlineIcon />
                                </Button>
                            </Box>
                        </Grid>
                    </Box>
                </Paper>
            </FormGroup>
        );
    }

    AnylationColumn(anylationDTO, key, disabled) {
        return (
            <Grid key={`anylation_` + key} item xs={12} container direction="row" spacing={1}>

                {this.AnylationRemoveButton(key, disabled)}
                {this.AnylationNameField(anylationDTO.nameRep, key, disabled)}
                {this.AnylationTypeSelector(anylationDTO.anylationType, key, disabled)}
                {this.AnylationTargetSelector(anylationDTO.targetMAnytyId, key, disabled)}
                {this.AnylationRequiredCheckbox(anylationDTO.required, key, disabled)}

            </Grid>
        );
    }

    AnylationRemoveButton(key, disabled) {
        return (
            <Grid item xs={1} container justify="center" alignContent="center">
                <Button
                    id={`_remove_anylation_${key}`}
                    disabled={disabled}
                    onClick={() => {
                        let anylations = this.state._manyty_anylations;
                        anylations.pop(key)

                        this.setState({
                            _manyty_anylations: anylations
                        });
                    }}
                >
                    <CancelOutlined />
                </Button>
            </Grid>
        );
    }

    AnylationNameField(anylationName, key, disabled) {
        return (
            <Grid item xs={5}>
                <TextField
                    id={`_anylation_column_name_${key}`}
                    size="small" fullWidth
                    label="Anylation Name"
                    disabled={disabled}
                    value={anylationName}
                    onChange={(event) => {
                        const anylations = this.state._manyty_anylations;
                        anylations[key - this.state.selectedParentAnylations]
                            .nameRep = event.target.value;

                        this.setState({
                            _manyty_anylations: anylations
                        });
                    }}
                />
            </Grid>
        );
    }

    AnylationTypeSelector(anylationType, key, disabled) {
        return (
            <Grid item xs={2}>
                <InputLabel shrink >
                    Anylation Type
                </InputLabel>
                <Select
                    id={`_anylation_type_${key}`}
                    size="small" fullWidth
                    displayEmpty
                    disabled={disabled}
                    value={anylationType}
                    onChange={(event) => {
                        let anylations = this.state._manyty_anylations;
                        anylations[key - this.state.selectedParentAnylations]
                            .anylationType = event.target.value;

                        this.setState({
                            _manyty_anylations: anylations
                        });
                    }}
                >
                    <MenuItem value={"reference"}>Reference</MenuItem>
                </Select>
            </Grid>
        );
    }

    AnylationTargetSelector(anylationTarget, key, disabled) {
        const targetOptions = [
            <MenuItem key={0} value={0}>None</MenuItem>,
            ...this.state.parentManyties.map((mAnyty) => {
                return (
                    <MenuItem key={mAnyty._manyty_id}
                        value={mAnyty._manyty_id}
                    >
                        {mAnyty.nameRep}
                    </MenuItem>
                );
            })]

        return (
            <Grid item xs={3}>
                <InputLabel shrink >
                    Anylation Target
                </InputLabel>
                <Select
                    id={`_anylation_target_${key}`}
                    size="small" fullWidth
                    displayEmpty
                    disabled={disabled}
                    value={anylationTarget}
                    onChange={(event) => {
                        let anylations = this.state._manyty_anylations;
                        anylations[key - this.state.selectedParentAnylations]
                            .targetMAnytyId = event.target.value;

                        this.setState({
                            _manyty_anylations: anylations
                        });
                    }}
                >
                    {targetOptions}
                </Select>
            </Grid>
        );
    }

    AnylationRequiredCheckbox(anylationRequired, key, disabled) {
        return (
            <Grid item xs={1} container justify="flex-end" direction="row">
                <InputLabel shrink>required</InputLabel>
                <Checkbox name="property"
                    id={`_anylation_required_${key}`}
                    checked={anylationRequired}
                    disabled={disabled}
                    onChange={() => {
                        let anylations = this.state._manyty_anybutes;
                        if (anylations[key - this.state.selectedParentAnylations].required) {
                            anylations[key - this.state.selectedParentAnylations].required = false;
                        } else {
                            anylations[key - this.state.selectedParentAnylations].required = true;
                        }

                        this.setState({
                            _manyty_anylations: anylations
                        });
                    }}
                />
            </Grid>
        );
    }
}
