import { Module } from '@nestjs/common';
import { LayoutController } from './layout.controller';

@Module({
  controllers: [LayoutController]
})
export class LayoutModule {}
