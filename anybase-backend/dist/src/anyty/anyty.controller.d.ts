import { AnytyDTO } from "./anyty.interface";
import { AnytyService } from "./anyty.service";
import { ModuleRef } from "@nestjs/core";
export declare class AnytyController {
    private moduleRef;
    private anytyProvider;
    constructor(moduleRef: ModuleRef, anytyProvider: AnytyService);
    createAnyty(anytyDTO: AnytyDTO, mAnytyId: number, response: any): Promise<void>;
    findAll(mAnytyId: number, response: any): Promise<void>;
    findOne(mAnytyId: number, anytyId: number, response: any): Promise<void>;
    deleteOne(mAnytyId: number, anytyId: number, response: any): Promise<void>;
}
