# Assistente de Primeiras Declarações — MVP PUC-Rio

Aplicação web desenvolvida como MVP (Produto Mínimo Viável) da pós-graduação em Desenvolvimento Full Stack da PUC-Rio, voltada à organização das informações utilizadas nas primeiras declarações de inventários e partilhas.

## Objetivo

Centralizar os dados do falecido, cônjuge, herdeiros, bens e dívidas em um fluxo de preenchimento guiado, reduzindo a repetição de informações e apoiando a elaboração dos demonstrativos patrimoniais.

## Funcionalidades

- Cadastro, consulta e edição dos dados do falecido.
- Cadastro, edição e exclusão de cônjuge, herdeiros, bens e dívidas.
- Consulta do inventário completo.
- Cálculos de meação e partilha conforme as regras implementadas.
- Auto de orçamento com os valores do patrimônio e sua distribuição.
- Estimativa acadêmica de ITCM, acessada pela rota `/itd-estimate` da API, identificada como ITD/RJ.
- Lista de conferência dos documentos necessários ao preenchimento.
- Folha de pagamento com os beneficiários e valores atribuídos no inventário.

A lista de documentos não realiza envio de arquivos. A folha de pagamento é um demonstrativo da distribuição de valores, sem transferências financeiras.

## Tecnologias e arquitetura

| Componente | Tecnologias |
| --- | --- |
| Frontend | HTML, CSS e JavaScript puro |
| Backend | Python e Flask |
| Banco de dados | SQLite, com persistência pelo SQLAlchemy |
| Validação dos dados | Pydantic |
| Comunicação | API REST por HTTP, com dados em JSON |
| Documentação da API | OpenAPI e Swagger, com flask-openapi3 |

O frontend recebe as informações preenchidas pelo usuário e envia requisições ao backend. O backend processa os dados, acessa o banco e retorna as respostas para exibição na interface.

## Repositórios

- [Backend — backend-inventario](https://github.com/Jtn2630/backend-inventario)
- [Frontend — frontend-inventario](https://github.com/Jtn2630/frontend-inventario)

Os projetos possuem repositórios Git separados. Localmente, podem ser organizados assim:

```text
mvp/
├── backend-inventario/
│   ├── .git/
│   ├── app.py
│   ├── requirements.txt
│   ├── database/
│   ├── tables_sql/
│   ├── api_data/
│   ├── routes/
│   ├── services/
│   └── README.md
└── frontend-inventario/
    ├── .git/
    ├── index.html
    ├── css/
    ├── js/
    │   ├── api.js
    │   └── app.js
    └── README.md
```

A pasta `mvp` é apenas organizadora, sem repositório Git próprio.

## Instalação

É necessário ter Python e Git instalados. Para obter uma nova cópia dos dois projetos, execute no PowerShell:

```powershell
mkdir mvp
cd mvp
git clone https://github.com/Jtn2630/backend-inventario.git backend-inventario
git clone https://github.com/Jtn2630/frontend-inventario.git frontend-inventario
```

Entre no backend, crie o ambiente virtual e ative-o:

```powershell
cd backend-inventario
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Para instalar as dependências do projeto, execute:

```powershell
pip install -r requirements.txt
```

As principais dependências são:

- **Flask:** aplicação web e API.
- **flask-openapi3:** integração com a documentação OpenAPI.
- **SQLAlchemy:** acesso e persistência no banco de dados.
- **Pydantic:** definição e validação dos dados.

O arquivo `requirements.txt` contém a lista completa de dependências e suas versões, incluindo Flask-CORS e o suporte ao Swagger.

O acesso ao SQLite está disponível na biblioteca padrão do Python pelo módulo `sqlite3`. Por isso, SQLite não entra no `requirements.txt` e não exige um servidor de banco separado. Os registros são armazenados no arquivo `database/inventory.db`.

## Execução

Com o ambiente virtual ativado, dentro da pasta `backend-inventario`, execute:

```powershell
python app.py
```

Mantenha o terminal aberto e acesse:

- [API — http://127.0.0.1:5000](http://127.0.0.1:5000)
- [Swagger — documentação interativa](http://127.0.0.1:5000/openapi/swagger)

Em seguida, abra `frontend-inventario/index.html` no navegador. O frontend utiliza HTML, CSS e JavaScript puro, sem necessidade de instalação de dependências com Node.js.

## Conexão entre frontend e backend

O endereço da API está configurado em `frontend-inventario/js/api.js`:

```javascript
const API_URL = "http://127.0.0.1:5000";
```

O JavaScript utiliza `fetch` para enviar requisições HTTP e receber respostas em JSON. Por exemplo, a consulta do inventário de identificador 1 utiliza:

```text
GET http://127.0.0.1:5000/inventory?deceased_id=1
```

A comunicação acontece pelo endereço da API, independentemente de os códigos estarem em repositórios separados. Com essa configuração, o backend deve estar em execução no mesmo computador do navegador, pois `127.0.0.1` representa a própria máquina. O backend utiliza Flask-CORS para permitir requisições do frontend a partir de outra origem.

## Principais rotas

| Método | Rota | Finalidade |
| --- | --- | --- |
| GET | `/` | Verificar a resposta da API |
| GET | `/deceased` | Listar falecidos e selecionar inventários |
| POST | `/deceased` | Cadastrar falecido |
| PUT | `/deceased/{id}` | Atualizar falecido |
| POST | `/spouse` | Cadastrar cônjuge |
| PUT / DELETE | `/spouse/{id}` | Atualizar ou excluir cônjuge |
| POST | `/heirs` | Cadastrar herdeiro |
| PUT / DELETE | `/heirs/{id}` | Atualizar ou excluir herdeiro |
| POST | `/assets` | Cadastrar bem |
| PUT / DELETE | `/assets/{id}` | Atualizar ou excluir bem |
| POST | `/debts` | Cadastrar dívida |
| PUT / DELETE | `/debts/{id}` | Atualizar ou excluir dívida |
| GET | `/inventory?deceased_id={id}` | Consultar inventário completo e resumo calculado |
| POST | `/itd-estimate` | Solicitar estimativa tributária |

`{id}` representa o identificador do registro. GET consulta dados; POST cadastra ou solicita processamento; PUT atualiza; DELETE exclui. Os campos de entrada e os modelos de resposta podem ser consultados no Swagger.
