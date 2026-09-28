# ==============================================================
# ARQUIVO: app.py
# Ponto de entrada da API Flask com suporte a OpenAPI 3 e CORS
# ==============================================================

# ==============================================================
# IMPORTAÇÕES NECESSÁRIAS
# ==============================================================
from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI

from database.database import create_database
from routes.inventory_routes import register_routes

# ==============================================================
# METADADOS DA DOCUMENTAÇÃO SWAGGER (OPENAPI)
# ==============================================================
info = Info(
    title="Estate Inventory API",
    version="1.0.0",
    description=(
        "API REST para cadastro e organização de inventários, "
        "cálculo de meação e partilha e estimativa de ITD/RJ."
    )
)

# Inicialização da aplicação OpenAPI
app = OpenAPI(
    __name__,
    info=info
)

# Habilita o CORS para requisições do front-end SPA
CORS(app)

# Criação do banco de dados e registro das rotas
create_database()
register_routes(app)

# ==============================================================
# ROTA DE VERIFICAÇÃO DE STATUS
# ==============================================================
@app.get(
    "/",
    summary="Verificar funcionamento da API"
)
def home():
    return {
        "message": "Estate Inventory API is running."
    }

# ==============================================================
# EXECUÇÃO DO SERVIDOR LOCAL
# ==============================================================
if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )