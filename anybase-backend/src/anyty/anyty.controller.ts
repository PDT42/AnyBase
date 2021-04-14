import { Body, Controller, Delete, Get, Param, Post, Res } from "@nestjs/common";
import { AnytyDTO } from "./anyty.interface";
import { AnytyService } from "./anyty.service";
import { ModuleRef } from "@nestjs/core";
import { MetaAnytyService } from "../meta-anyty/meta-anyty.service";

@Controller("anyty")
export class AnytyController {

  constructor(
    private moduleRef: ModuleRef,
    private anytyProvider: AnytyService
  ) {
  }

  /**
   * Create a new MetaAnyty.
   *
   * @param anytyDTO
   * @param mAnytyId
   * @param response
   */
  @Post("/create")
  async createAnyty(
    @Body() anytyDTO: AnytyDTO,
    @Res() response) {

    // TODO: Add validation for input data

    if (!(anytyDTO.mAnytyId && anytyDTO.mAnytyId > 0)) {
      throw new Error("No valid MetaAnyty specified!");
    }
    await this.moduleRef.get(MetaAnytyService, { strict: false }).getOne(anytyDTO.mAnytyId)
      .then(async (mAnyty) => {

        if (!mAnyty) {
          throw new Error("Specified MetaAnyty does not exist!");
        }

        await this.anytyProvider.createAnyty(mAnyty, anytyDTO)
          .then(() => response.status(200))
          .catch(r => {
            console.error(r);
            response.status(400);
          }).finally(() => response.send());

      }).catch((r) => {
        console.error(r);
        response.status(400);
      }).finally(() => response.send());
  }

  /**
   * Get all MetaAnyties.
   *
   * @param mAnytyId
   * @param response
   */
  @Get(":manyty_id/all")
  async findAll(
    @Param("manyty_id") mAnytyId: number,
    @Res() response) {

    await this.moduleRef.get(MetaAnytyService, { strict: false }).getOne(mAnytyId)
      .then(async (mAnyty) => {
        await this.anytyProvider.getAll(mAnyty, []).then((result) => {
          response.json(result);
          response.status(200);
        });
      }).catch((r) => {
        console.error(r);
        response.status(400);
      }).finally(() => response.send());
  }

  /**
   * Get detailed data on one Anyty.
   *
   * @param mAnytyId
   * @param anytyId
   * @param response
   */
  @Get(":manyty_id/:anyty_id/details")
  async findOne(
    @Param("manyty_id") mAnytyId: number,
    @Param("anyty_id") anytyId: number,
    @Res() response) {

    await this.moduleRef.get(MetaAnytyService, { strict: false }).getOne(mAnytyId)
      .then(async (mAnyty) => {
        await this.anytyProvider.getOne(mAnyty, anytyId).then((result) => {

          // TODO: Anyty does not exist

          response.json(result);
          response.status(200);
        });
      }).catch((r) => {
        console.error(r);
        response.status(400);
      }).finally(() => response.send());
  }

  /**
   * Delete an Anyty from the database.
   *
   * @param mAnytyId
   * @param anytyId
   * @param response
   */
  @Delete(":manyty_id/:anyty_id/delete")
  async deleteOne(
    @Param("manyty_id") mAnytyId: number,
    @Param("anyty_id") anytyId: number,
    @Res() response) {

    await this.moduleRef.get(MetaAnytyService, { strict: false }).getOne(mAnytyId)
      .then(async (mAnyty) => {
        await this.anytyProvider.delete(mAnyty, anytyId);
      }).catch((r) => {
        console.error(r);
        response.status(400);
      }).finally(() => response.send());
  }
}
