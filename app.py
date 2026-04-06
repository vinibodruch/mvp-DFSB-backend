from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI
from src.routes.task_routes import bp as tasks_bp

info = Info(
    title="Todo API",
    version="1.0.0",
    description="Aplicação de exemplo para gerenciamento de tarefas"
)

app = OpenAPI(__name__, info=info)
CORS(app)
app.register_api(tasks_bp)

@app.get("/health", responses={"200": {"description": "Aplicação está saudável"}})
def health():
    """
    Rota de verificação de saúde da aplicação.
    """
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(port=8080)