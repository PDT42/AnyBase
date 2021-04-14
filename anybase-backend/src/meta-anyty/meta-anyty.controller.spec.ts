import { Test, TestingModule } from '@nestjs/testing';
import { MetaAnytyController } from './meta-anyty.controller';

describe('MetaAnytyController', () => {
  let controller: MetaAnytyController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [MetaAnytyController],
    }).compile();

    controller = module.get<MetaAnytyController>(MetaAnytyController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
