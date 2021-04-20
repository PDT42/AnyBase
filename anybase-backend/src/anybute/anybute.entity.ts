import { Column, Entity, ManyToOne, PrimaryGeneratedColumn } from "typeorm";
import { MetaAnyty } from "../meta-anyty/meta-anyty.entity";

const SQLITE_REGEX = /([ &])/g;

@Entity()
export class Anybute {
  /**
   *
   */
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ nullable: false })
  columnName: string;

  @Column({ nullable: false })
  nameRep: string;

  @Column({ nullable: false })
  dataType: string;

  @Column({ nullable: false })
  required: boolean;

  @ManyToOne(() => MetaAnyty, (metaAnyty) => metaAnyty.anybutes)
  metaAnyty: MetaAnyty;
}

export interface AnybuteDTO {
  nameRep: string;
  dataType: string;
  required: boolean;
}

export function createAnybute(
  columnName: string,
  nameRep: string,
  dataType: string,
  metaAnyty: MetaAnyty
): Anybute {
  const newAnybute = new Anybute();

  newAnybute.columnName = columnName.replace(SQLITE_REGEX, "").toLowerCase();
  newAnybute.nameRep = nameRep;
  newAnybute.dataType = dataType;
  newAnybute.metaAnyty = metaAnyty;

  return newAnybute;
}
