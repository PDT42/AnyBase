import { Injectable } from '@nestjs/common';
import { ModuleRef } from '@nestjs/core';
import { Connection, getRepository } from 'typeorm';
import { FieldMapping, Layout, LayoutColumn, LayoutColumnDTO, LayoutDTO, LayoutRow, LayoutRowDTO } from './layout.entity';

@Injectable()
export class LayoutService {

    constructor(
        private moduleRef: ModuleRef,
        private connection: Connection
    ) { }

    async createLayout(layoutDTO: LayoutDTO): Promise<Layout> {
        // TODO: Implement

        const dbConnection = this.connection.createEntityManager();

        // Convert DTO to actual object
        let newLayout: Layout = new Layout();

        // TODO: Extract into separate functions

        newLayout.layoutRows = layoutDTO.layoutRows.map((layoutRowDTO: LayoutRowDTO) => {

            // Convert DTO to actual object
            let layoutRow: LayoutRow = new LayoutRow();

            layoutRow.layout = newLayout;
            layoutRow.layoutColumns = layoutRowDTO.layoutColumns.map((layoutColumnDTO: LayoutColumnDTO) => {

                // Convert DTO to actual object
                let layoutColumn: LayoutColumn = new LayoutColumn();

                layoutColumn.layoutComponentId = layoutColumnDTO.layoutComponentId;
                layoutColumn.width = layoutColumnDTO.width;
                layoutColumn.layoutRow = layoutRow;
                layoutColumn.fieldMappings = layoutColumnDTO.fieldMappings.map(([fieldId, columnName]: [string, string]) => {

                    // Convert string tuple to FieldMapping
                    let fieldMapping: FieldMapping = new FieldMapping();

                    // TODO: Add validation and error handling 
                    fieldMapping.metaAnytyId = layoutDTO.mAnytyId;
                    fieldMapping.anytyId = layoutDTO.anytyId;
                    fieldMapping.fieldId = fieldId;
                    fieldMapping.columnName = columnName;

                    return fieldMapping;
                });

                return layoutColumn;
            });

            return layoutRow;
        });

        // Store and return the new layout
        return await dbConnection.save(newLayout);
    }

    async getLayout(mAnytyId: number, anytyId: number = 0): Promise<Layout> {
        return await getRepository(Layout).findOne({
            where: `mAnytyId = ${mAnytyId} AND anytyId = ${anytyId}`,
            relations: [
                "layoutRows", "layoutRows.layoutColumns",
                "layoutRows.layoutColumns.fieldMappings"
            ]
        });
    }
}
