import { MetaAnytyService } from "./meta-anyty.service";
import { MetaAnytyDTO } from "./meta-anyty.entity";
import { ModuleRef } from "@nestjs/core";
export declare class MetaAnytyController {
    private moduleRef;
    private mAnytyProvider;
    constructor(moduleRef: ModuleRef, mAnytyProvider: MetaAnytyService);
    findAllMAnyties(response: any): Promise<void>;
    createMAnyty(metaAnytyDTO: MetaAnytyDTO, response: any): Promise<void>;
    findOneMAnyty(response: any, mAnytyId: number): Promise<void>;
}
