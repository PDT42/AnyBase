import React from "react";

import { TitleRow } from "../components/title-row";


interface UsersProps {

}

interface UsersState {

}

export class Users extends React.Component<UsersProps, UsersState> {

    constructor(props: UsersProps) {
        super(props);
        this.state = {};
    }

    render() {
        return (
            <div>
                <TitleRow titleText="Users" />
            </div>
        );
    }
}
