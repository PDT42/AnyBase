"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const testing_1 = require("@nestjs/testing");
const meta_anyty_controller_1 = require("./meta-anyty.controller");
describe('MetaAnytyController', () => {
    let controller;
    beforeEach(async () => {
        const module = await testing_1.Test.createTestingModule({
            controllers: [meta_anyty_controller_1.MetaAnytyController],
        }).compile();
        controller = module.get(meta_anyty_controller_1.MetaAnytyController);
    });
    it('should be defined', () => {
        expect(controller).toBeDefined();
    });
});
//# sourceMappingURL=meta-anyty.controller.spec.js.map