import { MetaAnyty } from '../meta-anyty/meta-anyty.entity';
export declare class Anybute {
    id: number;
    columnName: string;
    nameRep: string;
    dataType: string;
    metaAnyty: MetaAnyty;
}
export interface AnybuteDTO {
    columnName: string;
    dataType: string;
}
export declare function createAnybute(columnName: string, nameRep: string, dataType: string, metaAnyty: MetaAnyty): Anybute;
