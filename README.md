# Atlético RS

Projeto web para apresentação de informações de um clube de futebol, com páginas estáticas e uma API desenvolvida em Python.

## Tecnologias

- HTML, CSS e JavaScript — interface web
- Python e Flask — servidor e API
- MySQL — banco de dados
- mysql-connector-python — conexão entre Python e MySQL

## Funcionalidades presentes no código

- Página inicial servida pelo Flask
- Consulta de jogadores: `GET /api/jogadores`
- Consulta da agenda de partidas: `GET /api/agenda`
- Consulta da diretoria: `GET /api/diretoria`

As rotas de consulta retornam dados em JSON. O banco também define uma tabela de contato, mas não há uma rota correspondente no `app.py` atual.

## Estrutura do projeto

```text
atletico_rs/
├── app.py                 # Aplicação Flask e endpoints da API
├── atletico_rs.sql        # Criação do banco, tabelas e registros de exemplo
├── requeriments.txt       # Dependências Python (nome atual do arquivo)
├── static/
│   ├── index.html         # Página inicial
│   ├── css/               # Estilos
│   ├── img/               # Imagens
│   └── js/                # Scripts do frontend
├── .env                   # Arquivo atualmente vazio
├── .gitignore             # Arquivo atualmente vazio
└── README.md
```

## Como executar localmente

### Pré-requisitos

- Python 3
- MySQL em execução
- Git (opcional, para clonar o projeto)

### 1. Clonar o repositório

```bash
git clone https://github.com/renansnog/atletico_rs.git
cd atletico_rs
```

### 2. Criar um ambiente virtual

No Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```bash
pip install -r requeriments.txt
```

### 4. Preparar o banco de dados

Execute o script `atletico_rs.sql` no MySQL Workbench ou em outro cliente MySQL. Ele cria o banco `atletico_rs`, as tabelas `jogadores`, `agenda`, `diretoria` e `contato`, e insere alguns jogadores de exemplo.

### 5. Configurar a conexão

No arquivo `app.py`, ajuste os parâmetros de `mysql.connector.connect()` para corresponderem ao seu servidor MySQL local (host, usuário e senha).

**Atenção:** não publique senhas ou outras credenciais no GitHub. Recomenda-se migrar essa configuração para variáveis de ambiente e adicionar `.env` e `.venv/` ao `.gitignore`.

### 6. Iniciar a aplicação

```bash
python app.py
```

Acesse `http://127.0.0.1:5000/` no navegador.

Para consultar a API, use, por exemplo, `http://127.0.0.1:5000/api/jogadores`.

## Banco de dados

| Tabela | Finalidade |
| --- | --- |
| `jogadores` | Dados dos jogadores e nomes de arquivos de fotos |
| `agenda` | Datas, horários, locais e adversários |
| `diretoria` | Cargos e integrantes da diretoria |
| `contato` | Rede social, telefone e e-mail |

## Observações

- A configuração atual usa `debug=True`, apropriado apenas para desenvolvimento local.
- A API depende de um MySQL local configurado e das tabelas criadas pelo script SQL.
- Este README documenta a estrutura identificada no repositório; não representa uma validação de execução em produção.

## Autor

[renansnog](https://github.com/renansnog)
