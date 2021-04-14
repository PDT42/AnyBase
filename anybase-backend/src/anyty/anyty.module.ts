import { Module } from "@nestjs/common";
import { AnytyService } from "./anyty.service";
import { AnytyController } from './anyty.controller';

@Module({
  providers: [AnytyService],
  exports: [AnytyService],
  controllers: [AnytyController]
})
export class AnytyModule {
}
