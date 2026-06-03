from fastapi import FastAPI
from .routes.rotas_usuario import router as rt_user
from .routes.rotas_agendamentos import router as rt_agen
from database.db import get_session,criar_tabelas

app = FastAPI(
    title="Sistema de Agendamento Inteligente",
    description="API assíncrona para gerenciamento de agendamentos e notificações.",
    version="1.0.0"
)
app.include_router(rt_user)
app.include_router(rt_agen)


@app.get('/')
def home():
    return {"mensagem": "API de Agendamento rodando com sucesso!"}