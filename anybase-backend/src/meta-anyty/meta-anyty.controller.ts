import { Body, Controller, Delete, Get, Param, Post, Res } from "@nestjs/common";
import { MetaAnytyService } from "./meta-anyty.service";
import { MetaAnytyDTO } from "./meta-anyty.entity";

@Controller("meta-anyty")
export class MetaAnytyController {
  constructor(
    private mAnytyProvider: MetaAnytyService
  ) {
  }

  /**
   * Get Route /meta-anyty/all - to get all existing MetaAnyties.
   *
   * @param response
   */
  @Get("all")
  async findAllMAnyties(@Res() response) {
    response.setHeader("Content-Type", "application/json");

    await this.mAnytyProvider.getAll()
      .then((result) => {
        response.status(200);
        response.json(result);
      }).catch(r => {
        console.error(r);
        response.status(400);
      });
  }

  /**
   * Post Route /meta-anyty/create - to create a new MetaAnyty
   * in the application database.
   *
   * @param metaAnytyDTO
   * @param response
   */
  @Post("create")
  async createMAnyty(
    @Body() metaAnytyDTO: MetaAnytyDTO,
    @Res() response) {

    // TODO: Add validation for input data

    await this.mAnytyProvider.createMAnyty(metaAnytyDTO)
      .then(() => response.status(200))
      .catch(r => {
        console.error(r);
        response.status(400);
      }).finally(response.send());
  }

  /**
   * Get Route /meta-anyty/:manyty_id - to get data on one MetaAnyty
   * in the application database.
   *
   * @param response
   * @param mAnytyId
   */
  @Get(":manyty_id")
  async findOneMAnyty(
    @Param("manyty_id") mAnytyId: number,
    @Res() response) {
    await this.mAnytyProvider.getOne(mAnytyId).then(result => {
      response.status(200);
      response.json(result);
    }).catch(r => {
      console.error(r);
      response.status(400);
    }).finally(response.send());
  }

  /**
   * Delete Route /meta-anyty/:manyty_id - to delete a MetaAnyty from
   * the application database.
   *
   * @param mAnytyId
   * @param response
   */
  @Delete(":manyty_id")
  async deleteOne(
    @Param("manyty_id") mAnytyId: number,
    @Res() response) {

    await this.mAnytyProvider.delete(mAnytyId).then(result => {
      response.status(200);
    }).catch(r => {
      console.error(r);
      response.status(400);
    }).finally(response.send());
  }

  @Post(":manyty_id/update")
  async updateMAnyty(@Body() metaAnytyDTO: MetaAnytyDTO, @Res() response) {

  }
}
