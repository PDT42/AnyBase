import { Grid } from "@material-ui/core";
import React from "react";
import { HDivider } from "./common-components"

import styles from "./common-styles.module.css"


export function TitleRow({ titleText }) {
    return (
        <div>
            <div className={styles.titleRow}>
                <span className={styles.titleText}>{titleText}</span>
            </div>
            <HDivider />
        </div>
    );
}

export class TitleRowButtons extends React.Component {
    render() {
        const buttons = this.props.buttons.map((button, index) => {
            return (<Grid item key={index}>{button}</Grid>);
        })

        return (
            <Grid container direction="column" spacing={1}>
                <Grid item container direction="row" alignItems="center">
                    <Grid item xs={8}>
                        <span className={styles.titleText}>{this.props.titleText}</span>
                    </Grid>
                    <Grid item xs={4} container direction="row" spacing={1} justify="flex-end">
                        {buttons}
                    </Grid>
                </Grid>
                <Grid item>
                    <HDivider />
                </Grid>
            </Grid>
        );
    }
}