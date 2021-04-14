import { Column, Entity, ManyToOne, OneToOne, PrimaryGeneratedColumn } from "typeorm";
import { MetaAnyty } from "../meta-anyty/meta-anyty.entity";

@Entity()
export class Anylation {

  @PrimaryGeneratedColumn()
  id: number;

  @Column({ nullable: false })
  columnName: string;

  @Column({ nullable: false })
  nameRep: string;

  @ManyToOne(type => MetaAnyty, metaAnyty => metaAnyty.anylations)
  metaAnyty: MetaAnyty;

  @OneToOne(() => MetaAnyty)
  targetMetaAnyty: MetaAnyty;
}

export class AnylationDTO {
  columnName: string;
}