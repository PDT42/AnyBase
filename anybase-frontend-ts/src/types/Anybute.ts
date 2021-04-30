import { MetaAnyty } from "./MetaAnyty";

export interface Anybute {
    nameRep: string;
    dataType: string;
    required: boolean;
    id?: number;
    columnName?: string;
    metaAnyty?: MetaAnyty;
    editable?: boolean;
}