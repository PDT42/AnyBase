"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const testing_1 = require("@nestjs/testing");
const anyty_controller_1 = require("./anyty.controller");
describe('AnytyController', () => {
    let controller;
    beforeEach(async () => {
        const module = await testing_1.Test.createTestingModule({
            controllers: [anyty_controller_1.AnytyController],
        }).compile();
        controller = module.get(anyty_controller_1.AnytyController);
    });
    it('should be defined', () => {
        expect(controller).toBeDefined();
    });
});
//# sourceMappingURL=anyty.controller.spec.js.map