import { Injectable } from "@nestjs/common";
import { Connection } from "typeorm";
import { changing } from "best-globals";
import { MetaAnyty } from "../meta-anyty/meta-anyty.entity";
import { Anybute } from "../anybute/anybute.entity";
import { Anylation } from "../anylation/anylation.entity";
import { Anyty, AnytyDTO } from "./anyty.interface";
import { MetaAnytyService } from "../meta-anyty/meta-anyty.service";
import { ModuleRef } from "@nestjs/core";

const TYPE_MAPPING: Map<string, string> = new Map([
  ["number", "REAL"],
  ["float", "REAL"],
  ["double", "REAL"],
  ["integer", "INTEGER"],
  ["int", "INTEGER"],
  ["id", "INTEGER"],
  ["datetime", "INTEGER"],
  ["string", "TEXT"],
  ["str", "TEXT"]
]);

@Injectable()
export class AnytyService {
  constructor(
    private moduleRef: ModuleRef,
    private connection: Connection
  ) {
  }

  /**
   * Create the database table required for storing Anyties
   * that are described by the supplied MetaAnyty.
   *
   * @param metaAnyty
   */
  async initAnyty(metaAnyty: MetaAnyty) {

    // Create basic create Query
    let createQuery = `CREATE TABLE IF NOT EXISTS _anyty_${metaAnyty.name} (`;

    // Add necessary id column
    createQuery += "_anyty_id INTEGER PRIMARY KEY,";
    createQuery += "_anyty_parent_id INTEGER DEFAULT 0,";

    // Add columns for Anybutes
    // ------------------------
    metaAnyty.anybutes.map((anybute: Anybute) => {

      let dataType = TYPE_MAPPING.get(anybute.dataType);

      createQuery += `${anybute.columnName} `;
      createQuery += `${dataType}`;
      createQuery += ",";
    });

    // Add columns for Anylations
    // --------------------------
    metaAnyty.anylations.map((anylation: Anylation) => {

      createQuery += `${anylation.columnName} `;
      createQuery += "INTEGER";
      createQuery += ",";
    });

    // Remove suffix ','
    createQuery = createQuery.slice(0, createQuery.length - 1);
    createQuery += ");";

    await this.execute(createQuery);
  }

  /**
   * Create a new Anyty in the application database.
   *
   * @param metaAnyty
   * @param anyty
   */
  async createAnyty(metaAnyty: MetaAnyty, anyty: AnytyDTO): Promise<number> {

    // TODO: Make this accept Anyty instead of AnytyDTO as input

    // Create Insert Query
    // -------------------
    let insertQuery: string = `INSERT INTO ${metaAnyty.anytyTableName}  (`;
    let anytyValues: any[] = [];

    // Add Anybute columns
    let anybuteColumnNames: string[] = [];
    const anybutesMap = new Map(anyty.anybutes);

    // Adding created/updated time to value map
    const created: number = new Date().getTime();
    anybutesMap.set("_anyty_created", created);
    anybutesMap.set("_anyty_updated", created);

    // Add Anybute Columns
    // -------------------
    metaAnyty.anybutes.map((anybute: Anybute) => {

        // Add column to query and column value to list of values
        anybuteColumnNames.push(anybute.columnName);
        insertQuery += `${anybute.columnName},`;

        let anybuteValue: any = anybutesMap.get(anybute.columnName);
        if (anybuteValue && TYPE_MAPPING.get(anybute.dataType) == "TEXT") {
          anybuteValue = `"${anybuteValue}"`;
        }
        if (!anybuteValue) anybuteValue = "NULL";

        anytyValues.push(anybuteValue);
      }
    );

    // Add Anylation Columns
    // ---------------------
    let anylationColumnNames: string[] = [];
    const anylationsMap = new Map(anyty.anybutes);
    metaAnyty.anylations.map((anylation: Anylation) => {

      // Add column to query and column value to list of values
      anylationColumnNames.push(anylation.columnName);
      anytyValues.push(anylationsMap.get(anylation.columnName));
      insertQuery += `${anylation.columnName},`;
    });

    // Consider _anyty_parent column if necessary
    // ------------------------------------------
    const mAnytyService = await this.moduleRef.get(MetaAnytyService, { strict: false });
    if (metaAnyty.parentMAnytyId && metaAnyty.parentMAnytyId > 0) {

      // Make sure Parent MAnyty is present
      if (!metaAnyty.parentMAnyty) {
        metaAnyty.parentMAnyty = await mAnytyService.getOne(metaAnyty.parentMAnytyId);
      }

      // If a Parent Anyty is specified - get it
      let parentAnyty: Anyty = null;
      if (anyty.parentAnytyId && anyty.parentAnytyId > 0) {
        parentAnyty = await this.getOne(metaAnyty.parentMAnyty, anyty.parentAnytyId);

        if (!parentAnyty) {
          throw new Error("The referenced Parent-Anyty does not exist!");
        }
      }

      // Add Parent Anyty Id
      if (metaAnyty.parentMAnyty) {
        insertQuery += "_anyty_parent_id,";

        if (parentAnyty) {
          anytyValues.push(parentAnyty._anyty_id);
        } else {
          // Extract relevant information
          let parentAnyty: AnytyDTO = {
            mAnytyId: metaAnyty.parentMAnytyId,
            anybutes: anyty.anybutes.filter(
              (anybute) => !anybuteColumnNames.includes(anybute[0])),
            anylations: anyty.anylations.filter(
              (anylation) => !anylationColumnNames.includes(anylation[0]))
          };

          // Create Parent in the database
          await mAnytyService.getOne(metaAnyty.parentMAnytyId)
            .then(async (parentMAnyty: MetaAnyty) => {
              anytyValues.push(await this.createAnyty(parentMAnyty, parentAnyty));
            });
        }
      }
    }

    // Add values to query
    insertQuery = insertQuery.slice(0, insertQuery.length - 1);
    insertQuery += ") VALUES (";
    insertQuery += anytyValues.join(",");
    insertQuery += ");";

    // Finally create the anyty in the database
    return await this.execute(insertQuery);
  }

  private async getSelected(metaAnyty: MetaAnyty, selectQuery: string) {

    // Query Anyties from the database
    let anyties: Anyty[] = await this.execute(selectQuery);

    // Merge Anyties with parents
    if (metaAnyty.parentMAnytyId) {
      if (!metaAnyty.parentMAnyty) {
        metaAnyty.parentMAnyty = await this.moduleRef.get(MetaAnytyService, {
          strict: false
        }).getOne(metaAnyty.parentMAnytyId);
      }
      anyties = await Promise.all(anyties.map(async (anyty: Anyty) => {
        return changing(await this.getOne(metaAnyty.parentMAnyty, anyty._anyty_parent_id), anyty);
      }));
    }
    return anyties;
  }

  /**
   * Get all Anyties of a certain MetaAnyty from the
   * application database.
   *
   * @param metaAnyty
   * @param where
   */
  async getAll(metaAnyty: MetaAnyty, where?: string[]): Promise<Anyty[]> {

    // Create Select Query ..
    let selectQuery = `SELECT * FROM ${metaAnyty.anytyTableName}`;
    if (where && where.length > 0) selectQuery += " WHERE " + where.join(" AND ") + ";";
    else selectQuery += ";";

    return this.getSelected(metaAnyty, selectQuery);
  }


  /**
   * Get one anyty from the application database.
   *
   * @param metaAnyty
   * @param anytyId
   * @param where
   */
  async getOne(metaAnyty: MetaAnyty, anytyId: number, where?: string[]): Promise<Anyty> {

    // Create Select Query ..
    let selectQuery = `SELECT * FROM ${metaAnyty.anytyTableName}`;
    selectQuery += ` WHERE _anyty_id=${anytyId} `;
    if (where && where.length > 0) selectQuery += where.join(" AND ") + ";";
    else selectQuery += ";";

    return (await this.getSelected(metaAnyty, selectQuery))[0];
  }

  /**
   * Delete an anyty from the application database.
   *
   * @param metaAnyty
   * @param anytyId
   */
  async delete(metaAnyty: MetaAnyty, anytyId: number) {

    let deleteQuery = `DELETE FROM ${metaAnyty.anytyTableName} WHERE _anyty_id=${anytyId};`;

    await this.execute(deleteQuery);
  }

  /**
   * Execute a query on the database connection.
   *
   * @param query
   * @param parameters
   * @private
   */
  private async execute(query: string, parameters?: any[]): Promise<any> {
    console.log(query);

    const queryRunner = this.connection.createQueryRunner();

    // Create a database Connection
    await queryRunner.connect();
    await queryRunner.startTransaction();

    let result = null;

    try {
      result = await queryRunner.query(query, parameters);
      await queryRunner.commitTransaction();
    } catch (err) {
      console.error(err);
      await queryRunner.rollbackTransaction();
    } finally {
      await queryRunner.release();
    }

    return result;
  }
}
