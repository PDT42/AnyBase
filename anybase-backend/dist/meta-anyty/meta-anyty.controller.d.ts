import { MetaAnytyService } from "./meta-anyty.service";
import { MetaAnytyDTO } from "./meta-anyty.entity";
export declare class MetaAnytyController {
    private mAnytyProvider;
    constructor(mAnytyProvider: MetaAnytyService);
    findAllMAnyties(response: any): Promise<void>;
    createMAnyty(metaAnytyDTO: MetaAnytyDTO, response: any): Promise<void>;
    findOneMAnyty(mAnytyId: number, response: any): Promise<void>;
    deleteOne(mAnytyId: number, response: any): Promise<void>;
    updateMAnyty(metaAnytyDTO: MetaAnytyDTO, response: any): Promise<void>;
}
