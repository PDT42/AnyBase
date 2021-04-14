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
const core_1 = require("@nestjs/core");
let MetaAnytyController = class MetaAnytyController {
    constructor(moduleRef, mAnytyProvider) {
        this.moduleRef = moduleRef;
        this.mAnytyProvider = mAnytyProvider;
    }
    async findAllMAnyties(response) {
        response.setHeader("Content-Type", "application/json");
        this.mAnytyProvider.getAll()
            .then((result) => {
            response.status(200);
            response.json(result);
        }).catch(r => {
            console.error(r);
            response.status(400);
        }).finally(() => response.send());
    }
    async createMAnyty(metaAnytyDTO, response) {
        this.mAnytyProvider.create(metaAnytyDTO)
            .then(() => response.status(200))
            .catch(r => {
            console.error(r);
            response.status(400);
        }).finally(() => response.send());
    }
    async findOneMAnyty(response, mAnytyId) {
        this.mAnytyProvider.getOne(mAnytyId).then(result => {
            response.status(200);
            response.json(result);
        }).catch(r => {
            console.error(r);
            response.status(400);
        });
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
    __param(0, common_1.Body()), __param(1, common_1.Res()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object, Object]),
    __metadata("design:returntype", Promise)
], MetaAnytyController.prototype, "createMAnyty", null);
__decorate([
    common_1.Get(":manyty_id"),
    __param(0, common_1.Res()), __param(1, common_1.Param("manyty_id")),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object, Number]),
    __metadata("design:returntype", Promise)
], MetaAnytyController.prototype, "findOneMAnyty", null);
MetaAnytyController = __decorate([
    common_1.Controller("meta-anyty"),
    __metadata("design:paramtypes", [core_1.ModuleRef,
        meta_anyty_service_1.MetaAnytyService])
], MetaAnytyController);
exports.MetaAnytyController = MetaAnytyController;
//# sourceMappingURL=meta-anyty.controller.js.map