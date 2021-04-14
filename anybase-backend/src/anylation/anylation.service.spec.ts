import { Test, TestingModule } from '@nestjs/testing';
import { AnylationService } from './anylation.service';

describe('AnylationService', () => {
  let service: AnylationService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [AnylationService],
    }).compile();

    service = module.get<AnylationService>(AnylationService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
