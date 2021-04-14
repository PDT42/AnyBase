"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AnytyModule = void 0;
const common_1 = require("@nestjs/common");
const anyty_service_1 = require("./anyty.service");
const anyty_controller_1 = require("./anyty.controller");
let AnytyModule = class AnytyModule {
};
AnytyModule = __decorate([
    common_1.Module({
        providers: [anyty_service_1.AnytyService],
        exports: [anyty_service_1.AnytyService],
        controllers: [anyty_controller_1.AnytyController]
    })
], AnytyModule);
exports.AnytyModule = AnytyModule;
//# sourceMappingURL=anyty.module.js.map