"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const testing_1 = require("@nestjs/testing");
const anyty_service_1 = require("./anyty.service");
describe('AnytyService', () => {
    let service;
    beforeEach(async () => {
        const module = await testing_1.Test.createTestingModule({
            providers: [anyty_service_1.AnytyService],
        }).compile();
        service = module.get(anyty_service_1.AnytyService);
    });
    it('should be defined', () => {
        expect(service).toBeDefined();
    });
});
//# sourceMappingURL=anyty.service.spec.js.map