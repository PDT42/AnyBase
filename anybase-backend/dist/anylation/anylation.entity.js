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
exports.AnylationDTO = exports.Anylation = void 0;
const typeorm_1 = require("typeorm");
const meta_anyty_entity_1 = require("../meta-anyty/meta-anyty.entity");
let Anylation = class Anylation {
};
__decorate([
    typeorm_1.PrimaryGeneratedColumn(),
    __metadata("design:type", Number)
], Anylation.prototype, "id", void 0);
__decorate([
    typeorm_1.Column({ nullable: false }),
    __metadata("design:type", String)
], Anylation.prototype, "columnName", void 0);
__decorate([
    typeorm_1.Column({ nullable: false }),
    __metadata("design:type", String)
], Anylation.prototype, "nameRep", void 0);
__decorate([
    typeorm_1.ManyToOne(type => meta_anyty_entity_1.MetaAnyty, metaAnyty => metaAnyty.anylations),
    __metadata("design:type", meta_anyty_entity_1.MetaAnyty)
], Anylation.prototype, "metaAnyty", void 0);
__decorate([
    typeorm_1.OneToOne(() => meta_anyty_entity_1.MetaAnyty),
    __metadata("design:type", meta_anyty_entity_1.MetaAnyty)
], Anylation.prototype, "targetMetaAnyty", void 0);
Anylation = __decorate([
    typeorm_1.Entity()
], Anylation);
exports.Anylation = Anylation;
class AnylationDTO {
}
exports.AnylationDTO = AnylationDTO;
//# sourceMappingURL=anylation.entity.js.map