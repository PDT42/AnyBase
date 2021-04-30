export interface Anyty {
    [key: string]: any;

    _anyty_id?: number;
    _anyty_parent_id?: number;
    _anyty_child_manyty_id?: number;
    _anyty_child_anyty_id?: number;
    _anyty_created?: Date;
    _anyty_updated?: Date;
}

export interface AnytyDTO {
    mAnytyId: number;
    anybutes: [string, any][];
    anylations: [string, any][];
    
    parentMAnytyId?: number;
    created?: number;
  }