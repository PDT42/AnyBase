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
   * POST route /anyty/create - to Create a new Anyty
   * in the application database.
   *
   * @param anytyDTO
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

        await this.anytyProvider.syncCreateAnyty(mAnyty, anytyDTO)
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
   * Get route /anyty/:manyty_id/all to get all Anyties
   * of one MetaAnyty from the application database.
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
        await this.anytyProvider.syncGetAnyties(mAnyty, []).then((result) => {
          response.json(result);
          response.status(200);
        });
      }).catch((r) => {
        console.error(r);
        response.status(400);
      }).finally(() => response.send());
  }

  /**
   * GET route /anyty/:manyty_id/details - to get detailed data
   * on one Anyty in the application database.
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
        await this.anytyProvider.syncGetAnyty(mAnyty, anytyId).then((result) => {

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
   * DELETE route /anyty/:manyty_id/delete - to Delete
   * an Anyty from the database.
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
        await this.anytyProvider.deleteAnyty(mAnyty, anytyId);
      }).catch((r) => {
        console.error(r);
        response.status(400);
      }).finally(() => response.send());
  }

  /**
   *  POST route /anyty/:manyty_id/update - to Update
   *  an Anyty in the database.
   */
  @Post(":manyty_id/:anyty_id/update")
  async updateAnyty(
    @Param("manyty_id") mAnytyId: number,
    @Param("anyty_id") anytyId: number,
    @Body() anytyDTO: AnytyDTO,
    @Res() response
  ) {
    // TODO
  }

  /**
   * GET route /anyty/:manyty_id/:anyty_id/bookings - to get all Bookings
   * of the specified anyty.
   *
   */
  @Get(":manyty_id/:anyty_id/bookings")
  async findAllBookings(
    @Param("manyty_id") mAnytyId: number,
    @Param("anyty_id") anytyId: number,
    @Res() response
  ) {
    // TODO
  }
}
