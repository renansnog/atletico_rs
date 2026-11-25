-- Execute uma vez em um banco de demonstração.
USE atletico_rs;

INSERT INTO jogadores (nome, idade, localNascimento, timesAnterior, foto) VALUES
('Leonel Messi', 37, 'Rosário, Argentina', 'Barcelona, PSG, Inter Miami', 'leonelMessi.png'),
('Carlos Andrade', 28, 'Porto Alegre, Brasil', 'Inter-SM, Esportivo, Caxias', 'carlosAndrade.png'),
('André Vieira', 30, 'Porto Alegre, Brasil', 'Grêmio, Aimoré', 'andreVieira.png'),
('Paulinho Sabiá', 24, 'João Pessoa, Brasil', 'Confiança', 'paulinhoSabia.png');

INSERT INTO agenda (data, horario, local, adversario) VALUES
('2026-12-05', '15:30', 'Estádio Municipal', 'União Serrana'),
('2026-12-12', '16:00', 'Arena do Vale', 'Esportivo do Vale');

INSERT INTO diretoria (cargo, nome) VALUES
('Presidente', 'Helena Duarte'),
('Vice-presidente', 'Marcelo Tavares'),
('Diretora de futebol', 'Patrícia Almeida');
