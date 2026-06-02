from fastapi import FastAPI
from .routes.rotas_usuario import router
from database.db import get_session,criar_tabelas

app = FastAPI(
    title="Sistema de Agendamento Inteligente",
    description="API assíncrona para gerenciamento de agendamentos e notificações.",
    version="1.0.0"
)
app.include_router(router)


@app.get('/')
def home():
    return {"mensagem": "API de Agendamento rodando com sucesso!"}