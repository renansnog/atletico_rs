CREATE DATABASE atletico_rs;
USE atletico_rs;

CREATE TABLE jogadores ( 
	id  int auto_increment primary key, 
    nome varchar(100),
    idade int,
    localNascimento varchar(100),
    timesAnterior varchar(300),
    foto varchar(200)
);

CREATE TABLE agenda ( 
	id int auto_increment primary key,
    data date,
    horario time,
    local varchar(200),
    adversario varchar(100)
);

CREATE TABLE diretoria ( 
	id int auto_increment primary key,
    cargo varchar(100),
    nome varchar(100)
);

CREATE TABLE contato (
	id int auto_increment primary key,
    redeSocial varchar(100),
    telefone varchar(50),
    email varchar(100)
);

use atletico_rs;

insert into jogadores values 
(default, 'Leonel Messi', 37, 'Rosário, Argentina', 'Barcelona, PSG, Inter Miami', 'leonelMessi.png');

insert into jogadores values 
(default, 'Carlos Andrade', 28, 'Porto Alegre, Brasil', 'Inter-SM, Esportivo, Caxias', 'carlosAndrade.png');

insert into jogadores values 
(default, 'André Vieira', 30, 'Porto Alegre, Brasil', 'Grêmio, Aimoré', 'andreVieira.png');

insert into jogadores values 
(default, 'Paulinho Sabiá', 24, 'João Pessoa, Brasil', 'Confiança', 'paulinhoSabia.png');