# Projeto_BD_p3
# 🐘 Controle de Estoque: Arquitetura Orientada a Banco de Dados

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-PL%2FpgSQL-F29111?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python_Client-Flask-blue?style=for-the-badge&logo=python&logoColor=white)

Este projeto é um sistema de gerenciamento de estoque desenhado com foco total em **Database-Driven Architecture**. O objetivo principal é demonstrar como transferir a lógica de negócio pesada, auditoria e cálculos da camada de aplicação (backend) diretamente para o Sistema Gerenciador de Banco de Dados (SGBD), garantindo maior performance, integridade e segurança.

O frontend web e o backend em Python (Flask) atuam apenas como uma interface leve, enquanto o **PostgreSQL** executa o trabalho pesado.

## 🧠 Arquitetura SQL e Regras de Negócio

Em vez de sobrecarregar a rede com múltiplos comandos `SELECT` e `UPDATE`, este sistema utiliza os recursos avançados do PostgreSQL:

### 1. Computed Views (Consultas Otimizadas)
* **`vw_relatorio_estoque`**: Uma `VIEW` que projeta os dados da tabela de produtos já calculando o valor patrimonial total (`quantidade * preco`) em tempo de execução. A aplicação Python não faz cálculos matemáticos, ela apenas consome a View pronta.

### 2. Stored Procedures (Transações e Operações em Lote)
Scripts em **PL/pgSQL** para isolar as transações DML (Data Manipulation Language) e reduzir o tráfego de rede:
* **`sp_atualizar_produto`** e **`sp_deletar_produto`**: Encapsulam a lógica de atualização e exclusão.
* **`sp_aplicar_desconto_geral`**: Processa a atualização de milhares de preços com um único comando `CALL` recebido do servidor web, eliminando a necessidade de loops do lado da aplicação.
* **`sp_aplicar_desconto_produto`**: Aplica lógicas financeiras percentuais diretamente no dado bruto.

### 3. Triggers & Functions (Auditoria Invisível e Imutável)
* **`fn_auditoria_preco` & `trg_monitora_preco`**: Um gatilho `AFTER UPDATE` que atua como um sistema de auditoria ("cão de guarda"). Sempre que o preço de um produto for alterado (seja pelo Python, por uma Procedure ou via terminal direto no banco), o trigger intercepta a transação e salva os estados `OLD.preco` e `NEW.preco` na tabela `log_preco`. A aplicação cliente nem sabe que essa tabela de auditoria existe, garantindo segurança contra fraudes.

## 🗄️ Esquema do Banco de Dados (DDL)

```sql
-- Tabela Principal de Domínio
CREATE TABLE produto (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade >= 0),
    preco DECIMAL(10, 2) NOT NULL CHECK (preco >= 0)
);

-- Tabela de Auditoria (Isolada da Aplicação)
CREATE TABLE log_preco (
    id SERIAL PRIMARY KEY,
    id_produto INT REFERENCES produto(id) ON DELETE CASCADE,
    preco_antigo DECIMAL(10, 2),
    preco_novo DECIMAL(10, 2),
    data_alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
