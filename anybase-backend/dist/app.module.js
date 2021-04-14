"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AppModule = void 0;
const common_1 = require("@nestjs/common");
const app_controller_1 = require("./app.controller");
const app_service_1 = require("./app.service");
const meta_anyty_module_1 = require("./meta-anyty/meta-anyty.module");
const layout_module_1 = require("./layout/layout.module");
const anybute_module_1 = require("./anybute/anybute.module");
const anyty_service_1 = require("./anyty/anyty.service");
const typeorm_1 = require("@nestjs/typeorm");
const anylation_service_1 = require("./anylation/anylation.service");
const anylation_module_1 = require("./anylation/anylation.module");
const anyty_module_1 = require("./anyty/anyty.module");
let AppModule = class AppModule {
};
AppModule = __decorate([
    common_1.Module({
        imports: [
            meta_anyty_module_1.MetaAnytyModule,
            layout_module_1.LayoutModule,
            anybute_module_1.AnybuteModule,
            typeorm_1.TypeOrmModule.forRoot({ autoLoadEntities: true }),
            anylation_module_1.AnylationModule,
            anyty_module_1.AnytyModule
        ], controllers: [app_controller_1.AppController],
        providers: [app_service_1.AppService, anyty_service_1.AnytyService, anylation_service_1.AnylationService]
    })
], AppModule);
exports.AppModule = AppModule;
//# sourceMappingURL=app.module.js.map