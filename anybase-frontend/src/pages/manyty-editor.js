import React from "react";
import { Grid, Checkbox, FormControl, FormControlLabel, FormGroup, Select, TextField, Button } from "@material-ui/core";
import AddCircleOutlineIcon from '@material-ui/icons/AddCircleOutline';

import styles from "../components/common/common-styles.module.css";

import { TitleRow } from "../components/common/title-row";
import { HDivider } from "../components/common/common-components";

export class MAnytyEditor extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        return (
            <div>
                <TitleRow titleText="Create Meta Anyty" />
                <div className={styles.flexColumn}>
                    {MAnytyDefaultForm()}
                    <HDivider />
                    {MAnytyParameterForm()}
                </div>
            </div>
        );
    }
}



function MAnytyDefaultForm() {
    let checked = false;

    return (
        <div className={styles.flexCard}>
            <Grid container spacing={2}>
                <Grid item xs={12}>
                    <TextField style={{ width: "100%" }} id="name" size="small" label="Name" />
                </Grid>
                <Grid item xs={12}>
                    <Select style={{ width: "100%" }} id="name" size="small" label="Name" />
                </Grid>
                <Grid item xs={6}></Grid>
                <Grid item xs={6}>
                    <FormControlLabel style={{ width: "100%" }} control={
                        <Checkbox checked={checked} name="property" />
                    } label="Property" />
                </Grid>
            </Grid>
        </div>
    );
}

function MAnytyParameterForm() {
    return (
        <div className={styles.flexColumn}>
            <Button variant="contained" color="primary" size="small">
                <AddCircleOutlineIcon />
            </Button>
            <FormGroup className={styles.flexCard}>
                <div className={styles.flexRow}>

                </div>
            </FormGroup>
        </div>
    );
}