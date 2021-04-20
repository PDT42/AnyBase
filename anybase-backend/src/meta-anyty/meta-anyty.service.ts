import { Injectable } from "@nestjs/common";
import { MetaAnyty, MetaAnytyDTO } from "./meta-anyty.entity";
import { AnytyService } from "../anyty/anyty.service";
import { Connection, getRepository } from "typeorm";
import { Anybute, AnybuteDTO, createAnybute } from "../anybute/anybute.entity";
import { ModuleRef } from "@nestjs/core";
import { Anylation, AnylationDTO } from "../anylation/anylation.entity";

@Injectable()
export class MetaAnytyService {

  constructor(
    private moduleRef: ModuleRef,
    private connection: Connection
  ) {
  }

  /**
   * Create a new MetaAnyty in the applications database.
   *
   * @param metaAnytyDTO
   */
  async createMAnyty(metaAnytyDTO: MetaAnytyDTO): Promise<MetaAnyty> {
    const SQLITE_REGEX = /([ &])/g;

    // TODO: This function needs way more error handling!
    // TODO: Split this function into multiple functions

    let dbConnection = this.connection.createEntityManager();

    //  Constructing a MetaAnyty from MetaAnytyDTO
    let newMetaAnyty = new MetaAnyty();
    let anyNames: string[] = [];

    newMetaAnyty.name = metaAnytyDTO.nameRep.replace(SQLITE_REGEX, "").toLowerCase();
    newMetaAnyty.nameRep = metaAnytyDTO.nameRep;
    newMetaAnyty.anytyTableName = `_anyty_${newMetaAnyty.name}`;
    newMetaAnyty.isProperty = metaAnytyDTO.isProperty || false;

    // Check if a metaAnyty with this name exists
    let exMetaAnyty = await dbConnection.findOne(MetaAnyty,
      { where: `name = "${newMetaAnyty.name}"` });
    if (exMetaAnyty) {
      throw new Error("Could not create MetaAnyty! A MetaAnyty with that name already exists!");
    }

    // Check if MAnyty has a parent and get it ..
    const parentId = metaAnytyDTO.parentMAnytyId;
    if (parentId && typeof parentId === "number" && parentId > 0) {

      // Get Parent MAnyty from the database
      let parentMetaAnyty: MetaAnyty = await dbConnection.findOne(MetaAnyty, {
        where: `_manyty_id = ${metaAnytyDTO.parentMAnytyId}`,
        relations: ["anybutes", "anylations"]
      });

      if (!parentMetaAnyty) {
        throw new Error("The specified parent does not exist!");
      } else {
        newMetaAnyty.parentMAnytyId = parentMetaAnyty._manyty_id;
        newMetaAnyty.parentMAnyty = parentMetaAnyty;
      }

      parentMetaAnyty.anybutes.map((pAnybute: Anybute) => {
        anyNames.push(pAnybute.columnName);
      });
    }

    // Anybutes ..
    // -----------
    // Get User supplied Anybutes
    newMetaAnyty.anybutes = metaAnytyDTO.anybutes.map((anyDTO: AnybuteDTO) => {

      // Creating the Anybute instance ..
      let newAnybute: Anybute = new Anybute();
      let anybuteName: string = "_" + anyDTO.nameRep
        .replace(SQLITE_REGEX, "").toLowerCase();

      // Making sure every anybuteName is unique
      if (anyNames.includes(anybuteName)) {
        throw new Error("There can't be more than one Anybute with the same name!");
      } else anyNames.push(anybuteName);

      // Convert AnybuteDTO to Anybute
      newAnybute.columnName = anybuteName;
      newAnybute.nameRep = anyDTO.nameRep;
      newAnybute.dataType = anyDTO.dataType;
      newAnybute.metaAnyty = newMetaAnyty;
      newAnybute.required = anyDTO.required;

      return newAnybute;
    });

    // Add required internal Anybutes
    [{
      columnName: "_anyty_created",
      nameRep: "Created",
      dataType: "datetime",
      metaAnyty: newMetaAnyty,
      required: true
    }, {
      columnName: "_anyty_updated",
      nameRep: "Updated",
      dataType: "datetime",
      metaAnyty: newMetaAnyty,
      required: true
    }].map((anybute: Anybute) => {
      if (!anyNames.includes(anybute.columnName)) {
        newMetaAnyty.anybutes.push(anybute);
      }
    });

    // Anylations ..
    // -------------
    newMetaAnyty.anylations = await Promise.all(metaAnytyDTO.anylations.map(
      async (anylationDTO: AnylationDTO) => {
        let newAnylation: Anylation = new Anylation();

        const anylationName = "_" + anylationDTO.nameRep
          .replace(SQLITE_REGEX, "").toLowerCase();

        // Making sure every anybuteName is unique
        if (anyNames.includes(anylationName)) {
          throw new Error("There can't be more than one Anybute with the same name!");
        } else anyNames.push(anylationName);

        // Check the target MAnyty exists and get it
        const targetMAnyty = await this.getOne(anylationDTO.targetMAnytyId);
        if (!targetMAnyty) {
          throw new Error("Specified target Meta Anyty does not exist!");
        }

        // Converting the AnylationDTO
        newAnylation.columnName = anylationName;
        newAnylation.nameRep = anylationDTO.nameRep;
        newAnylation.metaAnyty = newMetaAnyty;
        newAnylation.anylationType = anylationDTO.anylationType;
        newAnylation.required = anylationDTO.required;
        newAnylation.targetMetaAnytyId = targetMAnyty._manyty_id;

        // Create the MAnyty that is intended to store
        // data on the Anylation between MAnyty and Target
        if (anylationDTO.anylationMAnytyDTO) {
          newAnylation.anylationMAnytyId = (await this.createMAnyty(
            anylationDTO.anylationMAnytyDTO))._manyty_id;
        } else newAnylation.anylationMAnytyId = 0;

        return newAnylation;
      })
    );

    // Handle Bookable MetaAnyty
    // -------------------------

    // Booking a Parent MAnyty means booking the Child MAnyty
    if (metaAnytyDTO.isBookable || (newMetaAnyty.parentMAnyty &&
      newMetaAnyty.parentMAnyty.bookingMAnytyId > 0)) {

      // Get the id of the parents booking MAnyty
      let bookingParentId: number = 0;
      if (newMetaAnyty.parentMAnyty) {
        bookingParentId = newMetaAnyty.parentMAnyty.bookingMAnytyId;
      }

      // Add default columns to the booking MAnyty
      let bookingAnybutes: AnybuteDTO[] = [];
      if (bookingParentId == 0) {
        bookingAnybutes = [
          { nameRep: "From", dataType: "datetime", required: true },
          { nameRep: "Until", dataType: "datetime", required: true }
        ];
      }

      // Create the booking MAnyty in the application database
      const bookingMAnyty: MetaAnyty = await this.createMAnyty({
        nameRep: `_booking_${newMetaAnyty.name}`,
        parentMAnytyId: bookingParentId,
        anybutes: bookingAnybutes,
        anylations: [],
        isProperty: true,
        isBookable: false
      });

      // Store new information
      newMetaAnyty.bookingMAnytyId = bookingMAnyty._manyty_id;
      newMetaAnyty.bookingMAnyty = bookingMAnyty;
    }
    // -------------------------

    // Creating the MetaAnyty in the database
    newMetaAnyty = await dbConnection.save(newMetaAnyty);

    // Creating a Table for the Anyties
    await this.moduleRef.get(AnytyService, { strict: false }).initAnyty(newMetaAnyty);

    return newMetaAnyty;
  }

  /**
   * Get a MetaAnyty from the database by id.
   *
   * @param manytyId
   */
  async getOne(manytyId: number): Promise<MetaAnyty> {
    return await getRepository(MetaAnyty).findOne({
      where: `_manyty_id = ${manytyId}`,
      relations: ["anybutes", "anylations"]
    });
  }

  /**
   * Get all MetaAnyties, that currently exist in the
   * application database.
   */
  async getAll(): Promise<MetaAnyty[]> {
    return await getRepository(MetaAnyty).find({
      where: "isProperty = 0",
      relations: ["anybutes", "anylations"]
    });
  }

  async getDescendants(mAnytyId: number): Promise<MetaAnyty[]> {
    return await getRepository(MetaAnyty).find({
      where: `parentMAnytyId = ${mAnytyId}`,
      relations: ["anybutes", "anylations"]
    });
  }

  /**
   * Delete a MAnyty from the application database.
   *
   * @param manytyId
   */
  async delete(manytyId: number): Promise<void> {
    const mAnyty: MetaAnyty = await this.getOne(manytyId);

    if (mAnyty) {
      await this.moduleRef.get(AnytyService, {
        strict: false
      }).deleteRecords(mAnyty);
      await getRepository(MetaAnyty).delete(`_manyty_id = ${manytyId}`);
    }
  }

  async update(manytyId: number, metaAnytyDTO: MetaAnytyDTO): Promise<void> {
    // TODO: update
  }
}