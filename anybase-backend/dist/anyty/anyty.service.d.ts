import { Connection } from "typeorm";
import { MetaAnyty } from "../meta-anyty/meta-anyty.entity";
import { Anyty, AnytyDTO } from "./anyty.interface";
import { ModuleRef } from "@nestjs/core";
export declare class AnytyService {
    private moduleRef;
    private connection;
    constructor(moduleRef: ModuleRef, connection: Connection);
    initAnyty(metaAnyty: MetaAnyty): Promise<void>;
    createAnyty(metaAnyty: MetaAnyty, anyty: AnytyDTO): Promise<number>;
    private getSelected;
    getAll(metaAnyty: MetaAnyty, where?: string[]): Promise<Anyty[]>;
    getOne(metaAnyty: MetaAnyty, anytyId: number, where?: string[]): Promise<Anyty>;
    delete(metaAnyty: MetaAnyty, anytyId: number): Promise<void>;
    private execute;
}
