# ==============================================================
# ARQUIVO: database/database.py
# Gerenciamento centralizado do banco de dados SQLite
# ==============================================================

# ==============================================================
# IMPORTAÇÕES NECESSÁRIAS
# ==============================================================
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Caminho e URL de conexão do SQLite
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "inventory.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Classe base para os modelos declarativos
class Base(DeclarativeBase):
    pass

# Configuração do engine e fábrica de sessões
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)

# ==============================================================
# INICIALIZAÇÃO DAS TABELAS NO BANCO
# ==============================================================
def create_database():
    """
    Importa as tabelas registradas e cria as estruturas no SQLite.
    """
    import tables_sql
    Base.metadata.create_all(bind=engine)