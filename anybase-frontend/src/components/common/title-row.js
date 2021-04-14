import { Button } from "@material-ui/core";

import styles from "./common-styles.module.css"

import { HDivider } from "../common/common-components"


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

export function TitleRowAddButton({ history, titleText }) {
    return (
        <div>
            <div className={styles.titleRow}>
                <span className={styles.titleText}>{titleText}</span>
                <div>
                    <Button className={styles.titleButton}
                        variant="contained"
                        color="primary"
                        size="medium"
                        onClick={() => history.push('/manyties/create')}
                    >add</Button>
                </div>
            </div>
            <HDivider />
        </div>
    );
}