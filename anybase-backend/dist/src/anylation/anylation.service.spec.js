"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const testing_1 = require("@nestjs/testing");
const anylation_service_1 = require("./anylation.service");
describe('AnylationService', () => {
    let service;
    beforeEach(async () => {
        const module = await testing_1.Test.createTestingModule({
            providers: [anylation_service_1.AnylationService],
        }).compile();
        service = module.get(anylation_service_1.AnylationService);
    });
    it('should be defined', () => {
        expect(service).toBeDefined();
    });
});
//# sourceMappingURL=anylation.service.spec.js.map