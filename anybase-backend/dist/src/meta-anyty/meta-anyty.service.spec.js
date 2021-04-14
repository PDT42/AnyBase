"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const testing_1 = require("@nestjs/testing");
const meta_anyty_service_1 = require("./meta-anyty.service");
describe('MetaAnytyService', () => {
    let service;
    beforeEach(async () => {
        const module = await testing_1.Test.createTestingModule({
            providers: [meta_anyty_service_1.MetaAnytyService],
        }).compile();
        service = module.get(meta_anyty_service_1.MetaAnytyService);
    });
    it('should be defined', () => {
        expect(service).toBeDefined();
    });
});
//# sourceMappingURL=meta-anyty.service.spec.js.map