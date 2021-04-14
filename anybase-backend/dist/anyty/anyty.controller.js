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
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AnytyController = void 0;
const common_1 = require("@nestjs/common");
const anyty_service_1 = require("./anyty.service");
const core_1 = require("@nestjs/core");
const meta_anyty_service_1 = require("../meta-anyty/meta-anyty.service");
let AnytyController = class AnytyController {
    constructor(moduleRef, anytyProvider) {
        this.moduleRef = moduleRef;
        this.anytyProvider = anytyProvider;
    }
    async createAnyty(anytyDTO, mAnytyId, response) {
        await this.moduleRef.get(meta_anyty_service_1.MetaAnytyService, { strict: false }).getOne(mAnytyId)
            .then(async (mAnyty) => {
            if (!mAnyty) {
                throw new Error("Specified MetaAnyty does not exist!");
            }
            await this.anytyProvider.createAnyty(mAnyty, anytyDTO)
                .then(() => response.status(200))
                .catch(r => {
                console.error(r);
                response.status(400);
            }).finally(() => response.send());
        }).catch((r) => {
            console.error(r);
            response.status(400);
        }).finally(() => response.send());
    }
    async findAll(mAnytyId, response) {
        await this.moduleRef.get(meta_anyty_service_1.MetaAnytyService, { strict: false }).getOne(mAnytyId)
            .then(async (mAnyty) => {
            await this.anytyProvider.getAll(mAnyty, []).then((result) => {
                response.json(result);
                response.status(200);
            });
        }).catch((r) => {
            console.error(r);
            response.status(400);
        }).finally(() => response.send());
    }
    async findOne(mAnytyId, anytyId, response) {
        await this.moduleRef.get(meta_anyty_service_1.MetaAnytyService, { strict: false }).getOne(mAnytyId)
            .then(async (mAnyty) => {
            await this.anytyProvider.getOne(mAnyty, anytyId).then((result) => {
                response.json(result);
                response.status(200);
            });
        }).catch((r) => {
            console.error(r);
            response.status(400);
        }).finally(() => response.send());
    }
    async deleteOne(mAnytyId, anytyId, response) {
        await this.moduleRef.get(meta_anyty_service_1.MetaAnytyService, { strict: false }).getOne(mAnytyId)
            .then(async (mAnyty) => {
            await this.anytyProvider.delete(mAnyty, anytyId);
        }).catch((r) => {
            console.error(r);
            response.status(400);
        }).finally(() => response.send());
    }
};
__decorate([
    common_1.Post(":manyty_id/create"),
    __param(0, common_1.Body()),
    __param(1, common_1.Param("manyty_id")),
    __param(2, common_1.Res()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object, Number, Object]),
    __metadata("design:returntype", Promise)
], AnytyController.prototype, "createAnyty", null);
__decorate([
    common_1.Get(":manyty_id/all"),
    __param(0, common_1.Param("manyty_id")),
    __param(1, common_1.Res()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Number, Object]),
    __metadata("design:returntype", Promise)
], AnytyController.prototype, "findAll", null);
__decorate([
    common_1.Get(":manyty_id/:anyty_id/details"),
    __param(0, common_1.Param("manyty_id")),
    __param(1, common_1.Param("anyty_id")),
    __param(2, common_1.Res()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Number, Number, Object]),
    __metadata("design:returntype", Promise)
], AnytyController.prototype, "findOne", null);
__decorate([
    common_1.Delete(":manyty_id/:anyty_id/delete"),
    __param(0, common_1.Param("manyty_id")),
    __param(1, common_1.Param("anyty_id")),
    __param(2, common_1.Res()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Number, Number, Object]),
    __metadata("design:returntype", Promise)
], AnytyController.prototype, "deleteOne", null);
AnytyController = __decorate([
    common_1.Controller("anyty"),
    __metadata("design:paramtypes", [core_1.ModuleRef,
        anyty_service_1.AnytyService])
], AnytyController);
exports.AnytyController = AnytyController;
//# sourceMappingURL=anyty.controller.js.map