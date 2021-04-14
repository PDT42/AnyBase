export interface Anyty {
  _anyty_id: number;
  _anyty_parent_id: number;
  _anyty_created: Date;
  _anyty_updated: Date;

  [key: string]: any;
}

export interface AnytyDTO {
  mAnytyId: number;
  parentMAnytyId?: number;
  parentAnytyId?: number;
  created?: number;
  // TODO: This will require more complexity!
  anybutes: [string, any][];
  anylations: [string, any][];
}