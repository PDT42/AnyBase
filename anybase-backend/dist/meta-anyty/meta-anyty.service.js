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
Object.defineProperty(exports, "__esModule", { value: true });
exports.MetaAnytyService = void 0;
const common_1 = require("@nestjs/common");
const meta_anyty_entity_1 = require("./meta-anyty.entity");
const anyty_service_1 = require("../anyty/anyty.service");
const typeorm_1 = require("typeorm");
const anybute_entity_1 = require("../anybute/anybute.entity");
const core_1 = require("@nestjs/core");
let MetaAnytyService = class MetaAnytyService {
    constructor(moduleRef, connection) {
        this.moduleRef = moduleRef;
        this.connection = connection;
    }
    async createMAnyty(metaAnytyDTO) {
        const SQLITE_REGEX = /([ &])/g;
        let dbConnection = this.connection.createEntityManager();
        let newMetaAnyty = new meta_anyty_entity_1.MetaAnyty();
        let anybuteNames = [];
        newMetaAnyty.name = metaAnytyDTO.name.replace(SQLITE_REGEX, "").toLowerCase();
        newMetaAnyty.nameRep = metaAnytyDTO.name;
        newMetaAnyty.tableName = `_anyty_${newMetaAnyty.name}`;
        newMetaAnyty.isProperty = metaAnytyDTO.isProperty;
        let exMetaAnyty = await dbConnection.findOne(meta_anyty_entity_1.MetaAnyty, { where: `name = "${newMetaAnyty.name}"` });
        if (exMetaAnyty) {
            throw new Error("Could not create MetaAnyty! A MetaAnyty with that name already exists!");
        }
        const parentId = metaAnytyDTO.parentMAnytyId;
        if (parentId && typeof parentId === "number" && parentId > 0) {
            let parentMetaAnyty = await dbConnection.findOne(meta_anyty_entity_1.MetaAnyty, {
                where: `_manyty_id = ${metaAnytyDTO.parentMAnytyId}`,
                relations: ["anybutes", "anylations"]
            });
            if (!parentMetaAnyty) {
                throw new Error("The specified parent does not exist!");
            }
            else {
                newMetaAnyty.parentMAnytyId = parentMetaAnyty._manyty_id;
                newMetaAnyty.parentMAnyty = parentMetaAnyty;
            }
            parentMetaAnyty.anybutes.map((pAnybute) => {
                anybuteNames.push(pAnybute.columnName);
            });
        }
        newMetaAnyty.anybutes = metaAnytyDTO.anybutes.map((anyDTO) => {
            let newAnybute = new anybute_entity_1.Anybute();
            let anybuteName = anyDTO.columnName
                .replace(SQLITE_REGEX, "").toLowerCase();
            if (anybuteName in anybuteNames) {
                throw new Error("There can't be more than one Anybute with the same name!");
            }
            else
                anybuteNames.push(anybuteName);
            newAnybute.columnName = anybuteName;
            newAnybute.nameRep = anyDTO.columnName;
            newAnybute.dataType = anyDTO.dataType;
            newAnybute.metaAnyty = newMetaAnyty;
            return newAnybute;
        });
        [
            anybute_entity_1.createAnybute("_anyty_created", "Created", "integer", newMetaAnyty),
            anybute_entity_1.createAnybute("_anyty_updated", "Updated", "integer", newMetaAnyty)
        ].map((anybute) => {
            if (!anybuteNames.includes(anybute.columnName))
                newMetaAnyty.anybutes.push(anybute);
        });
        newMetaAnyty.anylations = [];
        await dbConnection.save(newMetaAnyty);
        await this.moduleRef.get(anyty_service_1.AnytyService, { strict: false }).initAnyty(newMetaAnyty);
    }
    async getOne(manytyId) {
        return await typeorm_1.getRepository(meta_anyty_entity_1.MetaAnyty).findOne({
            where: `_manyty_id = ${manytyId}`,
            relations: ["anybutes", "anylations"]
        });
    }
    async getAll() {
        return await typeorm_1.getRepository(meta_anyty_entity_1.MetaAnyty).find({
            where: "isProperty = 0",
            relations: ["anybutes", "anylations"]
        });
    }
    async delete(manytyId) {
        await typeorm_1.getRepository(meta_anyty_entity_1.MetaAnyty).delete(`_manyty_id = ${manytyId}`);
    }
    async update(manytyId, metaAnytyDTO) {
    }
};
MetaAnytyService = __decorate([
    common_1.Injectable(),
    __metadata("design:paramtypes", [core_1.ModuleRef,
        typeorm_1.Connection])
], MetaAnytyService);
exports.MetaAnytyService = MetaAnytyService;
//# sourceMappingURL=meta-anyty.service.js.map