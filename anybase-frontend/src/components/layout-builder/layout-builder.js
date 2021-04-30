import React from "react";

export class StaticLayoutBuilder extends React.Component {

    // interface LayoutField {
    //     componentId: number,
        
    // }
    
    // interface Layout {
    //     layoutRows: Array<LayoutField[]>,
    //     manytyId: number,
    //     anytyId?: Number,
    // }
    

    constructor(props) {
        super(props);

        if(!this.props.layout) {
            throw new Error("The Layout builder requires a layout!")
        }
    }

    render() {

    }
}