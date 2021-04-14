import { Test, TestingModule } from '@nestjs/testing';
import { MetaAnytyService } from './meta-anyty.service';

describe('MetaAnytyService', () => {
  let service: MetaAnytyService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [MetaAnytyService],
    }).compile();

    service = module.get<MetaAnytyService>(MetaAnytyService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
