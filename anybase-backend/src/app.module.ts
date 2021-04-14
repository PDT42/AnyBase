import { Module } from "@nestjs/common";
import { AppController } from "./app.controller";
import { AppService } from "./app.service";
import { MetaAnytyModule } from "./meta-anyty/meta-anyty.module";
import { LayoutModule } from "./layout/layout.module";
import { AnybuteModule } from "./anybute/anybute.module";
import { AnytyService } from "./anyty/anyty.service";
import { TypeOrmModule } from "@nestjs/typeorm";
import { AnylationService } from "./anylation/anylation.service";
import { AnylationModule } from "./anylation/anylation.module";
import { AnytyModule } from "./anyty/anyty.module";

@Module({
  imports: [
    MetaAnytyModule,
    LayoutModule,
    AnybuteModule,
    TypeOrmModule.forRoot({ autoLoadEntities: true }),
    AnylationModule,
    AnytyModule
  ], controllers: [AppController],
  providers: [AppService, AnytyService, AnylationService]
})
export class AppModule {

}
