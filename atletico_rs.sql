CREATE DATABASE IF NOT EXISTS atletico_rs CHARACTER SET utf8mb4;
USE atletico_rs;

CREATE TABLE IF NOT EXISTS jogadores (
	id  int auto_increment primary key,
    nome varchar(100),
    idade int,
    localNascimento varchar(100),
    timesAnterior varchar(300),
    foto varchar(200)
);

CREATE TABLE IF NOT EXISTS agenda (
	id int auto_increment primary key,
    data date,
    horario time,
    local varchar(200),
    adversario varchar(100)
);

CREATE TABLE IF NOT EXISTS diretoria (
	id int auto_increment primary key,
    cargo varchar(100),
    nome varchar(100)
);

CREATE TABLE IF NOT EXISTS contato (
	id int auto_increment primary key,
    redeSocial varchar(100),
    telefone varchar(50),
    email varchar(100)
);
