import { Column, Entity, JoinTable, OneToMany, PrimaryGeneratedColumn } from "typeorm";
import { Anybute, AnybuteDTO } from "../anybute/anybute.entity";
import { Anylation, AnylationDTO } from "../anylation/anylation.entity";


@Entity()
export class MetaAnyty {

  /**
   * This is the Database Scheme for a MetaAnyty.
   */

  @PrimaryGeneratedColumn()
  _manyty_id: number;

  @Column({ nullable: false })
  name: string;

  @Column({ nullable: false })
  nameRep: string;

  @Column({ nullable: false })
  anytyTableName: string;

  @Column({ default: 0 })
  bookingMAnytyId: number;

  bookingMAnyty: MetaAnyty;

  @OneToMany(() => Anybute, anybute => anybute.metaAnyty, {
    cascade: true
  }) @JoinTable()
  anybutes: Anybute[];

  @OneToMany(() => Anylation, anylation => anylation.metaAnyty, {
    cascade: true
  }) @JoinTable()
  anylations: Anylation[];

  @Column({ nullable: false, default: 0 })
  parentMAnytyId: number;

  parentMAnyty: MetaAnyty;

  @Column({ nullable: false })
  isProperty: boolean;
}

export interface MetaAnytyDTO {
  nameRep: string;
  parentMAnytyId: number;
  anybutes: AnybuteDTO[];
  anylations: AnylationDTO[];
  isProperty: boolean;
  isBookable: boolean;
}
