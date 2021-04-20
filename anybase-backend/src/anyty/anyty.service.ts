import { Injectable } from "@nestjs/common";
import { Connection, QueryRunner } from "typeorm";
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

const REQUIRED_COLUMN_NAMES: string[] = [
  "_anyty_id",
  "_anyty_parent_id",
  "_anyty_child_manyty_id",
  "_anyty_child_anyty_id"
];

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
    createQuery += "_anyty_child_manyty_id INTEGER DEFAULT 0,";
    createQuery += "_anyty_child_anyty_id INTEGER DEFAULT 0,";

    // Add columns for Anybutes
    // ------------------------
    metaAnyty.anybutes.map((anybute: Anybute) => {

      let dataType = TYPE_MAPPING.get(anybute.dataType.toLowerCase());

      createQuery += `${anybute.columnName} `;
      createQuery += `${dataType}`;
      createQuery += ",";
    });

    // Add columns for Anylations
    // --------------------------
    metaAnyty.anylations.map((anylation: Anylation) => {

      let dataType = TYPE_MAPPING.get("id");

      createQuery += `${anylation.columnName} `;
      createQuery += `${dataType}`;
      createQuery += ",";
    });

    // Remove suffix ','
    createQuery = createQuery.slice(0, createQuery.length - 1);
    createQuery += ");";

    await this.execute(createQuery);
  }

  /**
   * Create an Anyty in the application database using one
   * transaction for all database interaction required.
   *
   * @param metaAnyty
   * @param anyty
   */
  async syncCreateAnyty(metaAnyty: MetaAnyty, anyty: AnytyDTO) {

    // TODO: Realize this using a decorator

    // Create a database Transaction
    const queryRunner = this.connection.createQueryRunner();
    await queryRunner.connect();
    await queryRunner.startTransaction();

    let result: number = 0;
    try {
      result = await this.createAnyty(metaAnyty, anyty, queryRunner);
      await queryRunner.commitTransaction();
    } catch (r) {
      console.error(r);
      await queryRunner.rollbackTransaction();
    } finally {
      await queryRunner.release();
    }

    return result;
  }

  /**
   * Create a new Anyty in the application database.
   *
   * @param metaAnyty
   * @param anyty
   * @param queryRunner
   */
  private async createAnyty(
    metaAnyty: MetaAnyty,
    anyty: AnytyDTO,
    queryRunner: QueryRunner):
    Promise<number> {

    // Create Insert Query
    // -------------------
    let insertQuery: string = `INSERT INTO ${metaAnyty.anytyTableName}  (`;
    let anytyValues: any[] = [];

    // Add Anybute Columns
    // -------------------
    let anybuteColumnNames: string[] = [];
    const anybutesMap: Map<string, any> = new Map(anyty.anybutes);

    // Adding created/updated time to value map
    const created: number = new Date().getTime();
    anybutesMap.set("_anyty_created", created);
    anybutesMap.set("_anyty_updated", created);

    metaAnyty.anybutes.map((anybute: Anybute) => {

        // Add column to query and column value to list of values
        anybuteColumnNames.push(anybute.columnName);
        insertQuery += `${anybute.columnName},`;

        let anybuteValue: any = anybutesMap.get(anybute.columnName);
        if (anybuteValue && TYPE_MAPPING.get(anybute.dataType.toLowerCase()) === "TEXT") {
          anybuteValue = `"${anybuteValue}"`;
        }
        if (!anybuteValue) anybuteValue = "NULL";

        anytyValues.push(anybuteValue);
      }
    );

    // Add Anylation Columns
    // ---------------------
    let anylationColumnNames: string[] = [];
    const anylationsMap: Map<string, any> = new Map(anyty.anybutes);
    metaAnyty.anylations.map((anylation: Anylation) => {

      // Add column to query and column value to list of values
      anylationColumnNames.push(anylation.columnName);
      insertQuery += `${anylation.columnName},`;

      // Get the anylation-value
      let anylationValue: number = anylationsMap.get(anylation.columnName);

      // Validation
      if (!anylationValue) {
        if (anylation.required) {
          throw new Error("Missing argument for anylation value!");
        } else anylationValue = 0;
      }

      if (!(typeof anylationValue === "number")) {
        throw new Error("Invalid argument for anylation value!");
      }

      // Determine what data needs to be stored
      switch (anylation.anylationType) {
        case "Reference": {
          // Anylation Column holds id of referenced Anyty
          anytyValues.push(anylationValue);
        }
      }

      if (!anylationValue) anylationValue = 0;
      anytyValues.push(anylationValue);
    });

    // Consider _anyty_parent column if necessary
    // ------------------------------------------
    let parentAnytyId: number = null;
    const mAnytyService = await this.moduleRef.get(MetaAnytyService, { strict: false });
    if (metaAnyty.parentMAnytyId && metaAnyty.parentMAnytyId > 0) {

      // Make sure Parent MAnyty is present
      if (!metaAnyty.parentMAnyty) {
        metaAnyty.parentMAnyty = await mAnytyService.getOne(metaAnyty.parentMAnytyId);
      }

      // Add Parent Anyty Id value
      if (metaAnyty.parentMAnyty) {
        insertQuery += "_anyty_parent_id,";

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
            parentAnytyId = await this.createAnyty(parentMAnyty, parentAnyty, queryRunner);
            anytyValues.push(parentAnytyId);
          });
      }
    }

    // Add values to query
    // -------------------
    insertQuery = insertQuery.slice(0, insertQuery.length - 1);
    insertQuery += ") VALUES (";
    insertQuery += anytyValues.join(",");
    insertQuery += ");";

    // Execute the INSERT query
    const newAnytyId: number = await queryRunner.query(insertQuery);

    // Update parent Anyty if necessary
    // --------------------------------
    if (metaAnyty.parentMAnytyId > 0 && parentAnytyId) {
      if (!metaAnyty.parentMAnyty) {
        metaAnyty.parentMAnyty = await mAnytyService.getOne(metaAnyty.parentMAnytyId);
      }

      const parentMAnyty = metaAnyty.parentMAnyty;
      const updateQuery: string = `UPDATE ${parentMAnyty.anytyTableName} SET ` +
        `_anyty_child_manyty_id = ${metaAnyty._manyty_id}, ` +
        `_anyty_child_anyty_id = ${newAnytyId} WHERE ` +
        `_anyty_id = ${parentAnytyId};`;
      await queryRunner.query(updateQuery);
    }

    return newAnytyId;
  }


  /**
   * Get all Anyties of a specified MetaAnyty, which fit where
   * from the database using one transaction for all interaction
   * required.
   *
   * @param metaAnyty
   * @param where
   */
  async syncGetAnyties(metaAnyty: MetaAnyty, where?: [string, string][]) {

    // Create a database Transaction
    const queryRunner = this.connection.createQueryRunner();
    await queryRunner.connect();
    await queryRunner.startTransaction();

    // create result variable
    let anyties: Anyty[] = [];

    try {
      anyties = await this.getAllAnyties(metaAnyty, queryRunner, where);
      await queryRunner.commitTransaction();
    } catch (r) {
      await queryRunner.rollbackTransaction();
      console.error(r);
    } finally {
      await queryRunner.release();
    }

    return anyties;
  }

  /**
   * Get all Anyties of a MetaAnyty from the database.
   *
   * @param metaAnyty
   * @param where
   * @param queryRunner
   * @private
   */
  async getAllAnyties(
    metaAnyty: MetaAnyty,
    queryRunner: QueryRunner,
    where?: [string, string][]):
    Promise<Anyty[]> {

    // Create Select Query ..
    // ----------------------
    let selectQuery = `SELECT * FROM ${metaAnyty.anytyTableName}`;

    let localWhere = this.resolveWhere(metaAnyty, where);
    if (localWhere) selectQuery += " WHERE " + localWhere + ";";
    else selectQuery += ";";

    // Run select query ..
    let $anyties: Promise<Anyty[]> = queryRunner.query(selectQuery);

    // Consider Parent MAnyty if necessary
    // -----------------------------------
    let $parentAnyties: Promise<Anyty[]> = null;
    if (metaAnyty.parentMAnytyId > 0) {

      // Make sure Parent MAnyty is present
      if (!metaAnyty.parentMAnyty) {
        metaAnyty.parentMAnyty = await this.moduleRef.get(MetaAnytyService, {
          strict: false
        }).getOne(metaAnyty.parentMAnytyId);
      }

      // Get relevant Parent Anyties
      where = where.filter(([columnName, _]) => {
        return columnName != "_anyty_child_manyty_id";
      });
      where.push(["_anyty_child_manyty_id", `= ${metaAnyty._manyty_id}`]);
      $parentAnyties = this.getAllAnyties(metaAnyty.parentMAnyty, queryRunner, where);
    }

    // Await and combine results
    // -------------------------
    let anyties: Anyty[] = await $anyties;

    const parentAnyties: Anyty[] = await $parentAnyties;
    if (parentAnyties) {
      const parentAnytyMap = new Map(
        parentAnyties.map((anyty: Anyty) => [anyty._anyty_id, anyty])
      );

      anyties = anyties.map((anyty: Anyty) => {
        return changing(parentAnytyMap.get(anyty._anyty_parent_id), anyty);
      }).filter((a) => a);
    }

    return anyties;
  }

  /**
   * Get an Anyty from the application database.
   *
   * @param metaAnyty
   * @param anytyId
   */
  async syncGetAnyty(metaAnyty: MetaAnyty, anytyId: number) {

    // Create a database Transaction
    const queryRunner = this.connection.createQueryRunner();
    await queryRunner.connect();
    await queryRunner.startTransaction();

    // create result variable
    let anyty: Anyty = null;

    try {
      anyty = await this.getAnyty(metaAnyty, anytyId, queryRunner);
      await queryRunner.commitTransaction();
    } catch (r) {
      await queryRunner.rollbackTransaction();
      console.error(r);
    } finally {
      await queryRunner.release();
    }

    return anyty;
  }

  /**
   * Get one anyty from the application database.
   *
   * @param metaAnyty
   * @param anytyId
   * @param queryRunner
   */
  private async getAnyty(
    metaAnyty: MetaAnyty,
    anytyId: number,
    queryRunner: QueryRunner):
    Promise<Anyty> {

    // Create Select Query ..
    let selectQuery = `SELECT * FROM ${metaAnyty.anytyTableName}`;
    selectQuery += ` WHERE _anyty_id=${anytyId};`;

    let anyty: Anyty = (await queryRunner.query(selectQuery))[0];

    if (anyty && metaAnyty.parentMAnytyId > 0) {
      if (!metaAnyty.parentMAnyty) {
        metaAnyty.parentMAnyty = await this.moduleRef.get(MetaAnytyService, {
          strict: false
        }).getOne(metaAnyty.parentMAnytyId);
      }

      let parentAnyty: Anyty = await this.getAnyty(
        metaAnyty.parentMAnyty, anyty._anyty_parent_id, queryRunner);
      anyty = changing(parentAnyty, anyty);
    }

    return anyty;
  }

  /**
   * Delete an anyty from the application database.
   *
   * @param metaAnyty
   * @param anytyId
   */
  async deleteAnyty(metaAnyty: MetaAnyty, anytyId: number) {

    let deleteQuery = `DELETE FROM ${metaAnyty.anytyTableName} WHERE _anyty_id=${anytyId};`;

    if (metaAnyty.parentMAnytyId > 0) {
      if (!metaAnyty.parentMAnyty) {
        metaAnyty.parentMAnyty = await this.moduleRef.get(MetaAnytyService, { strict: false })
          .getOne(metaAnyty.parentMAnytyId);
      }

      const anyty = await this.syncGetAnyty(metaAnyty, anytyId);

      if (anyty) await this.deleteAnyty(metaAnyty.parentMAnyty, anyty._anyty_parent_id);
    }

    await this.execute(deleteQuery);
  }

  /**
   * Delete all Anyties of metaAnyty where is true.
   *
   * @param metaAnyty
   * @param where
   * @param queryRunner
   */
  private async deleteAnytiesOf(
    metaAnyty: MetaAnyty,
    where: [string, string][],
    queryRunner: QueryRunner) {
    let deleteQuery = `DELETE FROM ${metaAnyty.anytyTableName} WHERE `;

    deleteQuery += this.resolveWhere(metaAnyty, where);
    deleteQuery += ";";

    await queryRunner.query(deleteQuery);
  }

  /**
   * Delete a previously created AnytyTable.
   *
   * @param metaAnyty
   */
  async deleteRecords(metaAnyty: MetaAnyty) {
    let deleteQuery = `DROP TABLE IF EXISTS ${metaAnyty.anytyTableName};`;

    const queryRunner = this.connection.createQueryRunner();

    // Create a database Connection
    await queryRunner.connect();
    await queryRunner.startTransaction();

    if (metaAnyty.parentMAnytyId > 0) {
      if (metaAnyty.parentMAnyty) {
        metaAnyty.parentMAnyty = await this.moduleRef.get(MetaAnytyService, {
          strict: false
        }).getOne(metaAnyty.parentMAnytyId);
      }
    }

    try {
      await queryRunner.query(deleteQuery);

      if (metaAnyty.parentMAnyty) await this.deleteAnytiesOf(metaAnyty.parentMAnyty, [
        ["_anyty_child_manyty_id", `= ${metaAnyty._manyty_id}`]
      ], queryRunner);

      await queryRunner.commitTransaction();
    } catch (err) {
      console.error(err);
      await queryRunner.rollbackTransaction();
    } finally {
      await queryRunner.release();
    }
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

  private resolveWhere(metaAnyty: MetaAnyty, where: [string, string][]) {
    let anybuteNames = metaAnyty.anybutes.map((anybute: Anybute) => anybute.columnName);
    anybuteNames.push(...REQUIRED_COLUMN_NAMES);
    let localWhere = where.map(([columnName, condition]) => {
      if (anybuteNames.includes(columnName)) {
        return `${columnName} ${condition}`;
      }
    }).filter((w) => w);

    return localWhere.join(" AND ");
  }
}

