# Atlético RS · v1.0.0

Sistema web de gestão esportiva para manter o elenco do Atlético RS, cadastrar e consultar partidas e consultar a diretoria. O MVP preserva a página institucional, as cores e as imagens do projeto original.

## Funcionalidades

| Área | Operações disponíveis |
| --- | --- |
| Jogadores | Cadastrar, listar, consultar por ID na API, editar e excluir com confirmação na tela |
| Agenda | Cadastrar e listar partidas por data e horário |
| Diretoria | Consultar integrantes e cargos |
| Demonstração | Carregar exemplos de elenco, partidas e diretoria com `demonstracao.sql` |

Os formulários ficam nas seções **Jogadores** e **Agenda**. A opção **Diretoria** no menu abre a consulta correspondente. O MVP foi projetado para uso local em `127.0.0.1`. A área de gestão não possui login. A seção Loja permanece como espaço reservado.

## Arquitetura e tecnologias

O Flask serve a página, os arquivos estáticos e a API JSON na mesma origem. A interface usa HTML, CSS e JavaScript e atualiza as listas após cada operação. O Flask valida os dados e utiliza o MySQL Connector/Python para executar consultas parametrizadas e confirmar as gravações. O MySQL armazena os registros nas tabelas `jogadores`, `agenda` e `diretoria`. A tabela `contato` foi preservada e a seção institucional de contato continua estática.

| Arquivo | Responsabilidade |
| --- | --- |
| `app.py` | Servidor Flask, API, integração com MySQL e validação |
| `static/` | Página, estilos, imagens e formulários JavaScript |
| `atletico_rs.sql` | Criação do banco e das tabelas sem apagar registros |
| `demonstracao.sql` | Dados de exemplo opcionais |
| `.env.example` | Modelo de configuração local do banco |
| `requirements.txt` | Dependências Python |

## Executar no Windows

Pré-requisitos: Git, Python 3.10 ou superior e MySQL Server em execução. O MySQL Workbench facilita executar os scripts SQL.

1. No PowerShell, clone o repositório e prepare o ambiente.

   ```powershell
   git clone https://github.com/renansnog/atletico_rs.git
   cd atletico_rs
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   Copy-Item .env.example .env
   ```

2. No MySQL Workbench, execute `atletico_rs.sql` na conexão local. Para uma instalação de demonstração vazia, execute também `demonstracao.sql` uma vez. Se já houver dados, use o banco existente e pule a carga de exemplo para evitar duplicatas.

3. Edite `.env` no VS Code. Preencha `DB_USER` e `DB_PASSWORD` com as credenciais locais e ajuste host e porta se necessário. Use uma conta MySQL com acesso ao banco `atletico_rs` e permissões de leitura e gravação para as operações descritas. O arquivo `.env` é ignorado pelo Git.

4. Volte ao PowerShell e inicie a aplicação.

   ```powershell
   .\.venv\Scripts\python.exe app.py
   ```

5. Abra [http://127.0.0.1:5000/](http://127.0.0.1:5000/) no navegador. Para encerrar, pressione **Ctrl+C** no terminal.

## API

| Endpoint | Métodos |
| --- | --- |
| `/api/jogadores` | `GET`, `POST` |
| `/api/jogadores/<id>` | `GET`, `PUT`, `DELETE` |
| `/api/agenda` | `GET`, `POST` |
| `/api/diretoria` | `GET` |

Envie gravações com `Content-Type: application/json`. Jogadores exigem `nome` e `idade`. Os campos opcionais são `localNascimento`, `timesAnterior` e `foto`. Partidas exigem `adversario`, `local`, `data` em `AAAA-MM-DD` e `horario` em `HH:MM`.

## Documentação e autoria

A [documentação técnica](docs/relatorio-tecnico.md) registra o diagnóstico, as contribuições de Renan Silva Nogueira e as alterações realizadas com auxílio de IA, além dos testes e das evidências da execução.
