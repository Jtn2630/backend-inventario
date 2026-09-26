# 📚 MVP — Sistema de Apoio à Elaboração de Inventário

---

## 📝 Etapas Concluídas

---

### 🔧 [Módulo Inicial — Ambiente e Estrutura]

1️⃣ Definição do MVP: sistema de apoio à elaboração de inventário e partilha.

2️⃣ Definição da arquitetura backend em Python com Flask.

3️⃣ Criação do ambiente virtual `.venv`.

4️⃣ Instalação e configuração das dependências iniciais:
- Flask
- SQLAlchemy
- Pydantic
- Flask-Cors
- flask-openapi3
- Swagger
- python-docx

5️⃣ Atualização do `pip` para a versão 26.2.1.

6️⃣ Validação das dependências com `python -m pip check`.

7️⃣ Definição da estrutura modular do backend:
- `database/`
- `tables_sql/`
- `api_data/`
- `routes/`
- `services/`

8️⃣ Definição das entidades iniciais do sistema:
- Falecido
- Cônjuge
- Herdeiro
- Bem

9️⃣ Definição do SQLite como banco de dados do MVP.

🔟 Definição do arquivo físico do banco dentro da pasta `database/`.

---

### 🔧 [Módulo de Banco de Dados]

1️⃣1️⃣ Estrutura inicial da pasta `database/`.

1️⃣2️⃣ Definição conceitual de:
- `Engine`
- `DeclarativeBase`
- `Session`
- `sessionmaker`

---

🔧 **Ponto atual: Etapa 12 — início da implementação da conexão com o banco SQLite.**