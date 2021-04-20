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
exports.MetaAnyty = void 0;
const typeorm_1 = require("typeorm");
const anybute_entity_1 = require("../anybute/anybute.entity");
const anylation_entity_1 = require("../anylation/anylation.entity");
let MetaAnyty = class MetaAnyty {
};
__decorate([
    typeorm_1.PrimaryGeneratedColumn(),
    __metadata("design:type", Number)
], MetaAnyty.prototype, "_manyty_id", void 0);
__decorate([
    typeorm_1.Column({ nullable: false }),
    __metadata("design:type", String)
], MetaAnyty.prototype, "name", void 0);
__decorate([
    typeorm_1.Column({ nullable: false }),
    __metadata("design:type", String)
], MetaAnyty.prototype, "nameRep", void 0);
__decorate([
    typeorm_1.Column({ nullable: false }),
    __metadata("design:type", String)
], MetaAnyty.prototype, "anytyTableName", void 0);
__decorate([
    typeorm_1.Column({ default: 0 }),
    __metadata("design:type", Number)
], MetaAnyty.prototype, "bookingMAnytyId", void 0);
__decorate([
    typeorm_1.OneToMany(() => anybute_entity_1.Anybute, anybute => anybute.metaAnyty, {
        cascade: true
    }),
    typeorm_1.JoinTable(),
    __metadata("design:type", Array)
], MetaAnyty.prototype, "anybutes", void 0);
__decorate([
    typeorm_1.OneToMany(() => anylation_entity_1.Anylation, anylation => anylation.metaAnyty, {
        cascade: true
    }),
    typeorm_1.JoinTable(),
    __metadata("design:type", Array)
], MetaAnyty.prototype, "anylations", void 0);
__decorate([
    typeorm_1.Column({ default: 0 }),
    __metadata("design:type", Number)
], MetaAnyty.prototype, "parentMAnytyId", void 0);
__decorate([
    typeorm_1.Column({ nullable: false }),
    __metadata("design:type", Boolean)
], MetaAnyty.prototype, "isProperty", void 0);
MetaAnyty = __decorate([
    typeorm_1.Entity()
], MetaAnyty);
exports.MetaAnyty = MetaAnyty;
//# sourceMappingURL=meta-anyty.entity.js.map