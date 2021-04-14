"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.MetaAnytyModule = void 0;
const common_1 = require("@nestjs/common");
const meta_anyty_service_1 = require("./meta-anyty.service");
const meta_anyty_controller_1 = require("./meta-anyty.controller");
const typeorm_1 = require("@nestjs/typeorm");
const meta_anyty_entity_1 = require("./meta-anyty.entity");
let MetaAnytyModule = class MetaAnytyModule {
};
MetaAnytyModule = __decorate([
    common_1.Module({
        imports: [typeorm_1.TypeOrmModule.forFeature([meta_anyty_entity_1.MetaAnyty])],
        exports: [typeorm_1.TypeOrmModule, meta_anyty_service_1.MetaAnytyService],
        providers: [meta_anyty_service_1.MetaAnytyService],
        controllers: [meta_anyty_controller_1.MetaAnytyController]
    })
], MetaAnytyModule);
exports.MetaAnytyModule = MetaAnytyModule;
//# sourceMappingURL=meta-anyty.module.js.map