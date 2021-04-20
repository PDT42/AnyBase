"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var _a, _b;
Object.defineProperty(exports, "__esModule", { value: true });
exports.AnytyService = void 0;
const common_1 = require("@nestjs/common");
const typeorm_1 = require("typeorm");
const best_globals_1 = require("best-globals");
const meta_anyty_service_1 = require("../meta-anyty/meta-anyty.service");
const core_1 = require("@nestjs/core");
const TYPE_MAPPING = new Map([
    ["number", "REAL"],
    ["float", "REAL"],
    ["double", "REAL"],
    ["integer", "INTEGER"],
    ["int", "INTEGER"],
    ["id", "INTEGER"],
    ["datetime", "INTEGER"],
    ["string", "TEXT"],
    ["str", "TEXT"]
]);
let AnytyService = class AnytyService {
    constructor(moduleRef, connection) {
        this.moduleRef = moduleRef;
        this.connection = connection;
    }
    async initAnyty(metaAnyty) {
        let createQuery = `CREATE TABLE IF NOT EXISTS _anyty_${metaAnyty.name} (`;
        createQuery += "_anyty_id INTEGER PRIMARY KEY,";
        createQuery += "_anyty_parent_id INTEGER DEFAULT 0,";
        metaAnyty.anybutes.map((anybute) => {
            let dataType = TYPE_MAPPING.get(anybute.dataType);
            createQuery += `${anybute.columnName} `;
            createQuery += `${dataType}`;
            createQuery += ",";
        });
        metaAnyty.anylations.map((anylation) => {
            createQuery += `${anylation.columnName} `;
            createQuery += "INTEGER";
            createQuery += ",";
        });
        createQuery = createQuery.slice(0, createQuery.length - 1);
        createQuery += ");";
        await this.execute(createQuery);
    }
    async createAnyty(metaAnyty, anyty) {
        let insertQuery = `INSERT INTO ${metaAnyty.anytyTableName}  (`;
        let anytyValues = [];
        let anybuteColumnNames = [];
        const anybutesMap = new Map(anyty.anybutes);
        const created = new Date().getTime();
        anybutesMap.set("_anyty_created", created);
        anybutesMap.set("_anyty_updated", created);
        metaAnyty.anybutes.map((anybute) => {
            anybuteColumnNames.push(anybute.columnName);
            insertQuery += `${anybute.columnName},`;
            let anybuteValue = anybutesMap.get(anybute.columnName);
            if (anybuteValue && TYPE_MAPPING.get(anybute.dataType) == "TEXT") {
                anybuteValue = `"${anybuteValue}"`;
            }
            if (!anybuteValue)
                anybuteValue = "NULL";
            anytyValues.push(anybuteValue);
        });
        let anylationColumnNames = [];
        const anylationsMap = new Map(anyty.anybutes);
        metaAnyty.anylations.map((anylation) => {
            anylationColumnNames.push(anylation.columnName);
            anytyValues.push(anylationsMap.get(anylation.columnName));
            insertQuery += `${anylation.columnName},`;
        });
        const mAnytyService = await this.moduleRef.get(meta_anyty_service_1.MetaAnytyService, { strict: false });
        if (metaAnyty.parentMAnytyId && metaAnyty.parentMAnytyId > 0) {
            if (!metaAnyty.parentMAnyty) {
                metaAnyty.parentMAnyty = await mAnytyService.getOne(metaAnyty.parentMAnytyId);
            }
            let parentAnyty = null;
            if (anyty.parentAnytyId && anyty.parentAnytyId > 0) {
                parentAnyty = await this.getOne(metaAnyty.parentMAnyty, anyty.parentAnytyId);
                if (!parentAnyty) {
                    throw new Error("The referenced Parent-Anyty does not exist!");
                }
            }
            if (metaAnyty.parentMAnyty) {
                insertQuery += "_anyty_parent_id,";
                if (parentAnyty) {
                    anytyValues.push(parentAnyty._anyty_id);
                }
                else {
                    let parentAnyty = {
                        mAnytyId: metaAnyty.parentMAnytyId,
                        anybutes: anyty.anybutes.filter((anybute) => !anybuteColumnNames.includes(anybute[0])),
                        anylations: anyty.anylations.filter((anylation) => !anylationColumnNames.includes(anylation[0]))
                    };
                    await mAnytyService.getOne(metaAnyty.parentMAnytyId)
                        .then(async (parentMAnyty) => {
                        anytyValues.push(await this.createAnyty(parentMAnyty, parentAnyty));
                    });
                }
            }
        }
        insertQuery = insertQuery.slice(0, insertQuery.length - 1);
        insertQuery += ") VALUES (";
        insertQuery += anytyValues.join(",");
        insertQuery += ");";
        return await this.execute(insertQuery);
    }
    async getSelected(metaAnyty, selectQuery) {
        let anyties = await this.execute(selectQuery);
        if (metaAnyty.parentMAnytyId) {
            if (!metaAnyty.parentMAnyty) {
                metaAnyty.parentMAnyty = await this.moduleRef.get(meta_anyty_service_1.MetaAnytyService, {
                    strict: false
                }).getOne(metaAnyty.parentMAnytyId);
            }
            anyties = await Promise.all(anyties.map(async (anyty) => {
                return best_globals_1.changing(await this.getOne(metaAnyty.parentMAnyty, anyty._anyty_parent_id), anyty);
            }));
        }
        return anyties;
    }
    async getAll(metaAnyty, where) {
        let selectQuery = `SELECT * FROM ${metaAnyty.anytyTableName}`;
        if (where && where.length > 0)
            selectQuery += " WHERE " + where.join(" AND ") + ";";
        else
            selectQuery += ";";
        return this.getSelected(metaAnyty, selectQuery);
    }
    async getOne(metaAnyty, anytyId, where) {
        let selectQuery = `SELECT * FROM ${metaAnyty.anytyTableName}`;
        selectQuery += ` WHERE _anyty_id=${anytyId} `;
        if (where && where.length > 0)
            selectQuery += where.join(" AND ") + ";";
        else
            selectQuery += ";";
        return (await this.getSelected(metaAnyty, selectQuery))[0];
    }
    async delete(metaAnyty, anytyId) {
        let deleteQuery = `DELETE FROM ${metaAnyty.anytyTableName} WHERE _anyty_id=${anytyId};`;
        await this.execute(deleteQuery);
    }
    async execute(query, parameters) {
        console.log(query);
        const queryRunner = this.connection.createQueryRunner();
        await queryRunner.connect();
        await queryRunner.startTransaction();
        let result = null;
        try {
            result = await queryRunner.query(query, parameters);
            await queryRunner.commitTransaction();
        }
        catch (err) {
            console.error(err);
            await queryRunner.rollbackTransaction();
        }
        finally {
            await queryRunner.release();
        }
        return result;
    }
};
AnytyService = __decorate([
    common_1.Injectable(),
    __metadata("design:paramtypes", [typeof (_a = typeof core_1.ModuleRef !== "undefined" && core_1.ModuleRef) === "function" ? _a : Object, typeof (_b = typeof typeorm_1.Connection !== "undefined" && typeorm_1.Connection) === "function" ? _b : Object])
], AnytyService);
exports.AnytyService = AnytyService;
//# sourceMappingURL=anyty.service.js.map