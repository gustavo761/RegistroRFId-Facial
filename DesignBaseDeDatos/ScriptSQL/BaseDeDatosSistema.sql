/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     12/3/2022 20:20:50                           */
/*==============================================================*/


drop table if exists CELULAR;

drop table if exists MATERIA;

drop table if exists PARALELO;

drop table if exists REGISTRO;

drop table if exists USUARIO;

/*==============================================================*/
/* Table: CELULAR                                               */
/*==============================================================*/
create table CELULAR
(
   CARNET               int not null,
   NUMERO               numeric(8,0)
);

/*==============================================================*/
/* Table: MATERIA                                               */
/*==============================================================*/
create table MATERIA
(
   IDMATERIA            int not null,
   CARNET               int not null,
   NOMBREMATERIA        varchar(50) not null,
   primary key (IDMATERIA)
);

/*==============================================================*/
/* Table: PARALELO                                              */
/*==============================================================*/
create table PARALELO
(
   IDPARALELO           int not null,
   IDMATERIA            int not null,
   HORAINICIO           time,
   HORASALIDA           time,
   NIVEL                varchar(20),
   primary key (IDPARALELO)
);

/*==============================================================*/
/* Table: REGISTRO                                              */
/*==============================================================*/
create table REGISTRO
(
   CARNET               int not null,
   FECHA                date,
   HORALLEGADA          time,
   HORAFINAL            time,
   MODOREGISTRO         varchar(10)
);

/*==============================================================*/
/* Table: USUARIO                                               */
/*==============================================================*/
create table USUARIO
(
   CARNET               int not null,
   NOMBRE               varchar(40) not null,
   APELLIDO             varchar(40) not null,
   TIPO                 varchar(20),
   TURNO                varchar(10),
   RFID                 varchar(20) not null,
   primary key (CARNET)
);

alter table CELULAR add constraint FK_RELATIONSHIP_1 foreign key (CARNET)
      references USUARIO (CARNET) on delete restrict on update restrict;

alter table MATERIA add constraint FK_DICTA foreign key (CARNET)
      references USUARIO (CARNET) on delete restrict on update restrict;

alter table PARALELO add constraint FK_TIENE foreign key (IDMATERIA)
      references MATERIA (IDMATERIA) on delete restrict on update restrict;

alter table REGISTRO add constraint FK_REALIZA foreign key (CARNET)
      references USUARIO (CARNET) on delete restrict on update restrict;

