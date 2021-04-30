import { Box, Grid, Paper } from "@material-ui/core";
import React from "react";
import styles from "./common-styles.module.css";
import { MetaAnyty } from "../types/MetaAnyty";

interface MAnytyListProps {
    history: any;
    metaAnyties: MetaAnyty[];
}

export class MAnytyList extends React.Component<MAnytyListProps, any> {

    onListItemNavigate = (mAnytyId: number) => {
        this.props.history.push(`/manyties/${mAnytyId}/details`);
    };

    render() {
        if (!this.props.metaAnyties) {
            return (
                <span>Loading ...</span>
            );
        }

        // Create a list item for each of the MAnyties
        const mAnytyList = this.props.metaAnyties.map((mAnyty, index) => {
            return (
                <MAnytyListItem key={mAnyty._manyty_id} mAnyty={mAnyty} mAnytyIndex={index}
                    onClick={() => this.onListItemNavigate(mAnyty._manyty_id!)}
                />
            );
        });

        return (
            <Grid container direction="column" spacing={2}>
                {mAnytyList}
            </Grid>
        );
    }
}

interface MAnytyListItemProps {
    mAnyty: MetaAnyty;
    mAnytyIndex: number;
    onClick: React.MouseEventHandler;
}

class MAnytyListItem extends React.Component<MAnytyListItemProps, any> {
    render() {
        return (
            <Grid item xs={12} key={this.props.mAnytyIndex}>
                <Paper className={styles.paperListItem}>
                    <Box p={1} onClick={this.props.onClick}>
                        <Grid container direction="column" spacing={1}>
                            <Grid item container direction="row" justify="space-between">
                                <Grid item>
                                    <span>{this.props.mAnyty.nameRep}</span>
                                </Grid>
                                <Grid item>
                                    <span>{this.props.mAnyty._manyty_id}</span>
                                </Grid>
                            </Grid>
                        </Grid>
                    </Box>
                </Paper>
            </Grid>
        );
    }
}