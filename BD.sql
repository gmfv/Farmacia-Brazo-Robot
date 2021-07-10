CREATE DATABASE if not exists BD_farmacia;
use BD_farmacia;

drop table if exists medicamentos;
CREATE TABLE medicamentos(
id int,
nombre VARCHAR(30),
descripcion VARCHAR(30),
foto VARCHAR(100),
precio INT,
stock INT,
primary key (id)
);