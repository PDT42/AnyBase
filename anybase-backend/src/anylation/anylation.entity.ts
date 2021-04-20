import { Column, Entity, JoinColumn, JoinTable, ManyToOne, OneToOne, PrimaryGeneratedColumn } from "typeorm";
import { MetaAnyty, MetaAnytyDTO } from "../meta-anyty/meta-anyty.entity";

@Entity()
export class Anylation {

  @PrimaryGeneratedColumn()
  id: number;

  @Column({ nullable: false })
  columnName: string;

  @Column({ nullable: false })
  nameRep: string;

  @ManyToOne(() => MetaAnyty, metaAnyty => metaAnyty.anylations)
  metaAnyty: MetaAnyty;

  @Column()
  targetMetaAnytyId: number;

  @Column({ nullable: false })
  anylationType: string;

  @Column({ nullable: false })
  required: boolean;

  @Column()
  anylationMAnytyId: number;
}

export class AnylationDTO {
  nameRep: string;
  anylationType: string; //TODO: Enumeration?
  targetMAnytyId: number;
  required: boolean;
  anylationMAnytyDTO?: MetaAnytyDTO;
}