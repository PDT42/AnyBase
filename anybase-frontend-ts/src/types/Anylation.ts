import { MetaAnyty } from "./MetaAnyty";

export interface Anylation {
    nameRep: string;
    anylationType: string;
    targetMetaAnytyId: number;
    required: boolean;
    id?: number;
    columnName?: string;
    metaAnyty?: MetaAnyty;
    anylationMAnytyId?: number;
    editable?: boolean;
}
