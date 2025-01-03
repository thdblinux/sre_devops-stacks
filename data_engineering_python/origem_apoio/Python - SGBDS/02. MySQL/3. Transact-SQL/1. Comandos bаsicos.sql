

#criando banco de dados 
CREATE DATABASE IF NOT EXISTS python;

#Criando tabela via script  
CREATE TABLE IF NOT EXISTS python.testepython (
    id INT ,
    nome VARCHAR(60)
    );

#verificando de tabela foi criada
select * from python.testepython;

#inserindo dados 
insert into python.testepython (id,nome) values (1,"Edmilson");

#verificando  dados inseridos
select * from python.testepython;

#Limpando dados
SET SQL_SAFE_UPDATES = 0;
DELETE FROM python.testepython WHERE nome = "Edmilson";

/*
Quando o modo de atualização segura está ativado, o MySQL exige que você use uma cláusula
 WHERE que inclua uma chave de índice ao executar operações de modificação de dados como UPDATE ou DELETE. 
 Essa medida é para garantir que você não atualize ou exclua todas as linhas em uma tabela sem a devida intenção.
*/


#Apagando tabela
drop table python.testepython;

USE python;

#Criando tabela via script  
CREATE TABLE IF NOT EXISTS testepython2 (
    id INT ,
    nome VARCHAR(60)
    );


#verificando de tabela foi criada
select * from testepython2;

#Apagando tabela
drop table testepython2;


#Apagando Banco de Dados
Drop database python






