import { Column, Entity, JoinTable, ManyToOne, OneToMany } from "typeorm";

@Entity()
export class Layout {

    @OneToMany(() => LayoutRow, layoutRow => layoutRow.layout, {
        cascade: true
    }) @JoinTable()
    layoutRows: LayoutRow[];
}

export interface LayoutDTO {
    mAnytyId: number;
    anytyId?: number;
    layoutRows: LayoutRowDTO[]
}

@Entity()
export class LayoutRow {

    @ManyToOne(() => Layout, layout => layout.layoutRows)
    layout: Layout;

    @OneToMany(() => LayoutColumn, layoutColumn => layoutColumn.layoutRow, {
        cascade: true
    }) @JoinTable()
    layoutColumns: LayoutColumn[];
}

export interface LayoutRowDTO {
    layoutColumns: LayoutColumnDTO[];
}

@Entity()
export class LayoutColumn {

    @ManyToOne(() => LayoutRow, layoutRow => layoutRow.layoutColumns)
    layoutRow: LayoutRow;

    @Column()
    width: number;

    @Column()
    layoutComponentId: string;

    @OneToMany(() => FieldMapping, fieldMapping => fieldMapping.layoutColumn, {
        cascade: true
    }) @JoinTable()
    fieldMappings: FieldMapping[]
}

export interface LayoutColumnDTO {
    width: number;
    layoutComponentId: string;
    fieldMappings: [string, string][];
}

@Entity()
export class FieldMapping {

    @ManyToOne(() => LayoutColumn, layoutColumn => layoutColumn.fieldMappings)
    layoutColumn: LayoutColumn;

    @Column({ nullable: false })
    metaAnytyId: number;

    @Column({ default: 0 })
    anytyId: number;

    @Column({ nullable: false })
    fieldId: string;

    @Column({ nullable: false })
    columnName: string;
}