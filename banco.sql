CREATE DATABASE imobiliaria;

CREATE TABLE imovel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    endereco VARCHAR(255) NOT NULL,
    cep VARCHAR(10) NOT NULL,
    valor_aluguel DECIMAL(10,2) NOT NULL,
    nome_proprietario VARCHAR(255) NOT NULL
);

CREATE TABLE inquilino (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(11) NOT NULL,
    telefone VARCHAR(15),
    data_nascimento DATE,
    imovel_id INT,
    FOREIGN KEY (imovel_id) REFERENCES imovel(id)
);
