import { Injectable } from "@nestjs/common";
import { ModuleRef } from "@nestjs/core";
import { AnylationDTO } from "./anylation.entity";

@Injectable()
export class AnylationService {

  constructor(
    private moduleRef: ModuleRef
  ) {
  }
}
