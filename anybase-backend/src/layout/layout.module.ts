import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { LayoutController } from './layout.controller';
import { FieldMapping, Layout, LayoutColumn, LayoutRow } from './layout.entity';
import { LayoutService } from './layout.service';

@Module({
  imports: [TypeOrmModule.forFeature([Layout, LayoutRow, LayoutColumn, FieldMapping])],
  controllers: [LayoutController],
  providers: [LayoutService]
})
export class LayoutModule { }
