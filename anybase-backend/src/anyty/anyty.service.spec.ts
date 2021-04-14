import { Test, TestingModule } from '@nestjs/testing';
import { AnytyService } from './anyty.service';

describe('AnytyService', () => {
  let service: AnytyService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [AnytyService],
    }).compile();

    service = module.get<AnytyService>(AnytyService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
