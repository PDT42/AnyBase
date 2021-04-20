import { Anybute, AnybuteDTO } from "../anybute/anybute.entity";
import { Anylation, AnylationDTO } from "../anylation/anylation.entity";
export declare class MetaAnyty {
    _manyty_id: number;
    name: string;
    nameRep: string;
    anytyTableName: string;
    bookingMAnytyId: number;
    bookingMAnyty: MetaAnyty;
    anybutes: Anybute[];
    anylations: Anylation[];
    parentMAnytyId: number;
    parentMAnyty: MetaAnyty;
    isProperty: boolean;
}
export interface MetaAnytyDTO {
    name: string;
    parentMAnytyId: number;
    anybutes: AnybuteDTO[];
    anylations: AnylationDTO[];
    isProperty: boolean;
    isBookable: boolean;
}
