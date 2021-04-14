import React from "react";
import { HDivider } from "../common/common-components";

import styles from "../common/common-styles.module.css";
import listStyles from "./item-list.module.css";


export function AnytyList({ history, listAnyties }) {

    function renderListAnyty(listAnyty) {
        return (
            <div key={listAnyty._manyty_id}>
                <div className={listStyles.listItem}
                    onClick={() => history.push('/manyties/' + listAnyty._manyty_id + '/details')}
                >
                    <div className={styles.flexColumn}>
                        <div className={styles.titleRow}>
                            <span>{listAnyty.nameRep}</span>
                            <span>{listAnyty._manyty_id}</span>
                        </div>
                        <HDivider />
                    </div>
                </div>
            </div >
        );
    }

    if (listAnyties) {
        return (
            <div className={listStyles.itemList}>
                {listAnyties.map((listAnyty) => renderListAnyty(listAnyty))}
            </div>
        );
    }
    return (
        <div>
            <span>No Data</span>
        </div>
    );

}