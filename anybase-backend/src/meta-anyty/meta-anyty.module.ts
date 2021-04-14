import { forwardRef, Module } from "@nestjs/common";
import { MetaAnytyService } from "./meta-anyty.service";
import { MetaAnytyController } from "./meta-anyty.controller";
import { TypeOrmModule } from "@nestjs/typeorm";
import { MetaAnyty } from "./meta-anyty.entity";
import { AnytyModule } from "../anyty/anyty.module";
import { AnytyService } from "../anyty/anyty.service";

@Module({
  imports: [TypeOrmModule.forFeature([MetaAnyty])],
  exports: [TypeOrmModule, MetaAnytyService],
  providers: [MetaAnytyService],
  controllers: [MetaAnytyController]
})
export class MetaAnytyModule {

}
