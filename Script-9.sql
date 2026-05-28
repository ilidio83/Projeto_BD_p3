CREATE TABLE produto (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    quantidade INT NOT NULL,
    preco DECIMAL(10, 2) NOT NULL
);

CREATE OR REPLACE VIEW vw_relatorio_estoque AS
SELECT 
    id, 
    nome, 
    quantidade, 
    preco, 
    (quantidade * preco) AS valor_patrimonio
FROM produto;

CREATE OR REPLACE PROCEDURE sp_aplicar_desconto_geral(p_percentual DECIMAL)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE produto 
    SET preco = preco - (preco * (p_percentual / 100));
END;
$$;
--Procedure para Atualizar um Produto
CREATE OR REPLACE PROCEDURE sp_atualizar_produto(
    p_id INT, 
    p_nome VARCHAR, 
    p_quantidade INT, 
    p_preco DECIMAL
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE produto 
    SET nome = p_nome, quantidade = p_quantidade, preco = p_preco
    WHERE id = p_id;
END;
$$;

-- Procedure para Deletar um Produto
CREATE OR REPLACE PROCEDURE sp_deletar_produto(p_id INT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM produto WHERE id = p_id;
END;
$$;

-- Procedure para Dar Desconto em um Produto Específico
CREATE OR REPLACE PROCEDURE sp_aplicar_desconto_produto(
    p_id INT, 
    p_percentual DECIMAL
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE produto 
    SET preco = preco - (preco * (p_percentual / 100))
    WHERE id = p_id;
END;
$$;
-- Cria a tabela para guardar o log)
CREATE TABLE log_preco (
    id SERIAL PRIMARY KEY,
    id_produto INT,
    preco_antigo DECIMAL(10, 2),
    preco_novo DECIMAL(10, 2),
    data_alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cria a função que o gatilho vai executar
CREATE OR REPLACE FUNCTION fn_auditoria_preco() 
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.preco <> OLD.preco THEN
        INSERT INTO log_preco (id_produto, preco_antigo, preco_novo)
        VALUES (OLD.id, OLD.preco, NEW.preco);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Cria o Trigger 
CREATE TRIGGER trg_monitora_preco
AFTER UPDATE ON produto
FOR EACH ROW
EXECUTE FUNCTION fn_auditoria_preco();