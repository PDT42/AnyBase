import { Module } from "@nestjs/common";
import { TypeOrmModule } from "@nestjs/typeorm";
import { Anybute } from "./anybute.entity";

@Module({
  imports: [TypeOrmModule.forFeature([Anybute])],
  exports:[TypeOrmModule]
})
export class AnybuteModule {}
