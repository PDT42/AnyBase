import { MetaAnyty, MetaAnytyDTO } from "./meta-anyty.entity";
import { Connection } from "typeorm";
import { ModuleRef } from "@nestjs/core";
export declare class MetaAnytyService {
    private moduleRef;
    private connection;
    constructor(moduleRef: ModuleRef, connection: Connection);
    getOne(manyty_id: number): Promise<MetaAnyty>;
    getAll(): Promise<MetaAnyty[]>;
    create(metaAnytyDTO: MetaAnytyDTO): Promise<void>;
}
