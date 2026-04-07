from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI

from src.models.database import init_db
from src.routes.task_routes import bp as tasks_bp

info = Info(
    title="To-Do List API",
    version="1.0.0",
    description=(
        "Aplicação de gerenciamento de tarefas, permitindo criar, ler, atualizar e excluir tarefas."
    ),
)

app = OpenAPI(__name__, info=info)
CORS(app,
    resources={r"/*": {"origins": "*"}}, # Permitir CORS para todas as origens
    methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"] # Permitir os métodos HTTP usados na API
)

app.register_api(tasks_bp)


@app.get("/health", tags=[], responses={200: {"description": "API is running"}})
def health():
    """Endpoint de saúde para verificar se a API está funcionando."""
    return {"status": "ok"}, 200


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=True, port=8080)
