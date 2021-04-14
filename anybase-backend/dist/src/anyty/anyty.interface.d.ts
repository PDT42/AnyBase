export interface Anyty {
    _anyty_id: number;
    _anyty_parent_id: number;
    _anyty_created: Date;
    _anyty_updated: Date;
    [key: string]: any;
}
export interface AnytyDTO {
    id?: number;
    parentId?: number;
    childId?: number;
    childMAnytyId?: number;
    created?: number;
    anybutes: [string, any][];
    anylations: [string, any][];
}
