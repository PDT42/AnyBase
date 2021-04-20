import { HDivider } from "../common/common-components"

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

export function TitleRowButton({ titleText, button }) {
    return (
        <div>
            <div className={styles.titleRow}>
                <span className={styles.titleText}>{titleText}</span>
                <div>{button}</div>
            </div>
            <HDivider />
        </div>
    );
}