import { Anybute } from "../types/Anybute";
import { Anylation } from "../types/Anylation";

export interface MetaAnyty {
    nameRep: string;
    anybutes: Anybute[];
    anylations: Anylation[];
    isBookable: boolean;
    isProperty: boolean;
    name?: string;
    anytyTableName?: string;

    bookingMAnytyId?: number;
    bookingMAnyty?: MetaAnyty;

    parentMAnytyId?: number;
    parentMAnyty?: MetaAnyty;

    _manyty_id?: number;
}