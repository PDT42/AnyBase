import { MetaAnyty, MetaAnytyDTO } from "./meta-anyty.entity";
import { Connection } from "typeorm";
import { ModuleRef } from "@nestjs/core";
export declare class MetaAnytyService {
    private moduleRef;
    private connection;
    constructor(moduleRef: ModuleRef, connection: Connection);
    createMAnyty(metaAnytyDTO: MetaAnytyDTO): Promise<MetaAnyty>;
    getOne(manytyId: number): Promise<MetaAnyty>;
    getAll(): Promise<MetaAnyty[]>;
    getDescendants(mAnytyId: number): Promise<MetaAnyty[]>;
    delete(manytyId: number): Promise<void>;
    update(manytyId: number, metaAnytyDTO: MetaAnytyDTO): Promise<void>;
}
