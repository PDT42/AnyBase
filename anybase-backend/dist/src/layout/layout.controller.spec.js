"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const testing_1 = require("@nestjs/testing");
const layout_controller_1 = require("./layout.controller");
describe('LayoutController', () => {
    let controller;
    beforeEach(async () => {
        const module = await testing_1.Test.createTestingModule({
            controllers: [layout_controller_1.LayoutController],
        }).compile();
        controller = module.get(layout_controller_1.LayoutController);
    });
    it('should be defined', () => {
        expect(controller).toBeDefined();
    });
});
//# sourceMappingURL=layout.controller.spec.js.map