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
        response.json(result);
        response.status(200);
      }).catch(r => {
        console.error(r);
        response.status(400);
      });
  }

  /**
   * Get Route /meta-anyty/anybutetypes - to get all
   * datatypes an anybute can possibly have.
   *
   * @param response
   */
  @Get("anybutetypes")
  async findAllAnybutetypes(@Res() response) {
    response.setHeader("Content-Type", "application/json");

    response.json([
      "String",
      "Integer",
      "Real",
      "Datetime",
      "Date"
    ]);
    response.status(200);
  }

  /**
   * Get Route /meta-anyty/anylationtypes - to get all
   * types an anyltion can possibly have.
   *
   * @param response
   */
  @Get("anylationtypes")
  async findAllAnylationtypes(@Res() response) {
    response.setHeader("Content-Type", "application/json");

    response.json([ //TODO: Enumeration?
      "Reference", // Anylation to an any other public MAnyty
      "ReferenceCollection", // Collection of any Anyties of any other public MAnyty

      // Limited in time reference to another Anyty of any other MAnyty.
      // The referenced Anyty must be of a bookable type. Referencing an
      // Anyty creates a booking of that anyty.
      "TReference",
      "TReferenceCollection"
    ]);
    response.status(200);
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
    response.setHeader("Content-Type", "application/json");

    await this.mAnytyProvider.getOne(mAnytyId).then(result => {
      response.json(result);
      response.status(200);
    }).catch(r => {
      console.error(r);
      response.status(400);
    });
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

    await this.mAnytyProvider.delete(mAnytyId).then(() => {
      response.status(200);
    }).catch(r => {
      console.error(r);
      response.status(400);
    });
  }

  @Post(":manyty_id/update")
  async updateMAnyty(@Body() metaAnytyDTO: MetaAnytyDTO, @Res() response) {

  }
}
