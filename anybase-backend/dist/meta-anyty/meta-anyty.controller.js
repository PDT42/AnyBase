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
exports.MetaAnytyController = void 0;
const common_1 = require("@nestjs/common");
const meta_anyty_service_1 = require("./meta-anyty.service");
let MetaAnytyController = class MetaAnytyController {
    constructor(mAnytyProvider) {
        this.mAnytyProvider = mAnytyProvider;
    }
    async findAllMAnyties(response) {
        response.setHeader("Content-Type", "application/json");
        await this.mAnytyProvider.getAll()
            .then((result) => {
            response.status(200);
            response.json(result);
        }).catch(r => {
            console.error(r);
            response.status(400);
        });
    }
    async createMAnyty(metaAnytyDTO, response) {
        await this.mAnytyProvider.createMAnyty(metaAnytyDTO)
            .then(() => response.status(200))
            .catch(r => {
            console.error(r);
            response.status(400);
        }).finally(response.send());
    }
    async findOneMAnyty(mAnytyId, response) {
        await this.mAnytyProvider.getOne(mAnytyId).then(result => {
            response.status(200);
            response.json(result);
        }).catch(r => {
            console.error(r);
            response.status(400);
        }).finally(response.send());
    }
    async deleteOne(mAnytyId, response) {
        await this.mAnytyProvider.delete(mAnytyId).then(result => {
            response.status(200);
        }).catch(r => {
            console.error(r);
            response.status(400);
        }).finally(response.send());
    }
    async updateMAnyty(metaAnytyDTO, response) {
    }
};
__decorate([
    common_1.Get("all"),
    __param(0, common_1.Res()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object]),
    __metadata("design:returntype", Promise)
], MetaAnytyController.prototype, "findAllMAnyties", null);
__decorate([
    common_1.Post("create"),
    __param(0, common_1.Body()),
    __param(1, common_1.Res()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object, Object]),
    __metadata("design:returntype", Promise)
], MetaAnytyController.prototype, "createMAnyty", null);
__decorate([
    common_1.Get(":manyty_id"),
    __param(0, common_1.Param("manyty_id")),
    __param(1, common_1.Res()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Number, Object]),
    __metadata("design:returntype", Promise)
], MetaAnytyController.prototype, "findOneMAnyty", null);
__decorate([
    common_1.Delete(":manyty_id"),
    __param(0, common_1.Param("manyty_id")),
    __param(1, common_1.Res()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Number, Object]),
    __metadata("design:returntype", Promise)
], MetaAnytyController.prototype, "deleteOne", null);
__decorate([
    common_1.Post(":manyty_id/update"),
    __param(0, common_1.Body()), __param(1, common_1.Res()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object, Object]),
    __metadata("design:returntype", Promise)
], MetaAnytyController.prototype, "updateMAnyty", null);
MetaAnytyController = __decorate([
    common_1.Controller("meta-anyty"),
    __metadata("design:paramtypes", [meta_anyty_service_1.MetaAnytyService])
], MetaAnytyController);
exports.MetaAnytyController = MetaAnytyController;
//# sourceMappingURL=meta-anyty.controller.js.map