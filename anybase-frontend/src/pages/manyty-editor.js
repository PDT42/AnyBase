import React from "react";
import { Paper, Grid, Checkbox, FormControlLabel, FormGroup, Select, TextField, Button, MenuItem, InputLabel, Box } from "@material-ui/core";
import AddCircleOutlineIcon from '@material-ui/icons/AddCircleOutline';

import styles from "../components/common/common-styles.module.css";

import { TitleRowButton } from "../components/common/title-row";
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
                anylationType: 'Reference',
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
                <Grid item xs={12}>
                    <TitleRowButton titleText="Create Meta Anyty" button={
                        <Button variant="contained"
                            color="secondary"
                            size="medium"
                            onClick={onSaveButtonClicked}
                        >Save</Button>
                    } />
                </Grid>

                {this.MAnytyDefaultForm()}
                <Grid item xs={12}>
                    <HDivider />
                </Grid>
                {this.MAnytyAnybuteForm()}
                <Grid item xs={12}>
                    <HDivider />
                </Grid>
                {this.MAnytyAnylationForm()}
            </Grid>
        );
    }

    // +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    MAnytyDefaultForm() {
        return (
            <Grid item xs={12}>
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
            </Grid>
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
                            selectedParentAnybutes: parent.anybutes.length || 0
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
            <Grid item xs={12}>
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
            </Grid>
        );
    }

    AnybuteColumn(anybuteDTO, key, disabled = false) {
        return (
            <Grid key={`anybute_${key}`} container direction="row" spacing={2}>
                <Grid item container justify="center" alignContent="center" xs={1}>
                    <CancelOutlined />
                </Grid>
                {this.AnybuteNameField(anybuteDTO.nameRep, key, disabled)}
                {this.AnybuteDataTypeSelector(anybuteDTO.dataType, key, disabled)}
                {this.AnybuteRequiredCheckbox(anybuteDTO.required, key, disabled)}
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

        // Create Anybute Columns for 
        // each Anybute already added
        const anylationColumns = this.state._manyty_anylations.map((anylationDTO, index) => {
            let key = index + parentAnylationColumns.length;
            return this.AnylationColumn(anylationDTO, key);
        });

        // Define a function to add a new Anybute
        let addAnybute = () => {
            let currentAnybutes = this.state._manyty_anybutes;

            //   nameRep: string;
            //   anylationType: string; //TODO: Enumeration?
            //   targetMAnytyId: number;
            //   required: boolean;
            //   anylationMAnytyDTO?: MetaAnytyDTO;

            currentAnybutes.push({
                nameRep: '',
                anylationType: 'Reference',
                required: false,
                targetMAnytyId: 0,
                anylationMAnytyDTO: {}
            });
            this.setState({ _manyty_anybutes: currentAnybutes })
        }

        // Define OnClick Handler
        let onAddButtonClick = () => {
            addAnybute();
        }

        return (
            <Grid item xs={12}>
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
                                        onClick={() => console.log('anylation add')}
                                    >
                                        <AddCircleOutlineIcon />
                                    </Button>
                                </Box>
                            </Grid>
                        </Box>
                    </Paper>
                </FormGroup>
            </Grid>
        );
    }

    AnylationColumn(anylationDTO, key, disabled) {
        return (
            <Grid key={`anylation_` + key} item xs={12} container direction="row" spacing={1}>
                <Grid item xs={6}>
                    {anylationDTO.anylationType}
                </Grid>
            </Grid>
        );
    }
}
