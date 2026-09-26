from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI

from database.database import create_database
from routes.inventory_routes import register_routes


info = Info(
    title="Estate Inventory API",
    version="1.0.0",
    description="API acadêmica para apoio à elaboração de inventário."
)

app = OpenAPI(
    __name__,
    info=info
)

CORS(app)

create_database()
register_routes(app)


@app.get(
    "/",
    summary="Verificar funcionamento da API"
)
def home():
    return {
        "message": "Estate Inventory API is running."
    }


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )