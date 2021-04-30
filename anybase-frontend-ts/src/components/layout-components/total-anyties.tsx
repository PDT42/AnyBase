import { Box, Grid, Paper } from "@material-ui/core";
import React from "react";

interface TotalAnytiesProps {
    totalAnyties: number;
}

export class TotalAnyties extends React.Component<TotalAnytiesProps, any> {
    render() {
        return (
            <Grid item>
                <Paper>
                    <Box p={1}>
                        <Grid container direction="row" justify="space-between">
                            <Grid item>
                                <span>Total Anyties on Record:</span>
                            </Grid>
                            <Grid>
                                <span>{this.props.totalAnyties}</span>
                            </Grid>
                        </Grid>
                    </Box>
                </Paper>
            </Grid>
        );
    }
}