import { Test, TestingModule } from '@nestjs/testing';
import { AnytyController } from './anyty.controller';

describe('AnytyController', () => {
  let controller: AnytyController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [AnytyController],
    }).compile();

    controller = module.get<AnytyController>(AnytyController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
