from fastapi import APIRouter,Depends,HTTPException
from sqlmodel import Session,select
from database.models.agendamentos import *
from database.models.usuario import *
from database.db import get_session

routes = APIRouter(prefix='/agendamentos',tags=['Agendamentos'])

#Agendar
@routes.post('/',response_model=AgendamentosRead)
def agendar(dados_agendamento:AgendamentosCreate,session: Session = Depends(get_session)):
    achar_usuario = session.exec(select(Usuarios).where(Usuarios.id_usuario == dados_agendamento.id_usuario)).first()
    if not achar_usuario:
        raise HTTPException(
            status_code=404,
            detail=f'Usuario com id {dados_agendamento.id_usuario} não encontrado.'
        )
    
    criar_agendamento = Agendamentos(**dados_agendamento.model_dump())
    try:
        session.add(criar_agendamento)
        session.commit()
        session.refresh(criar_agendamento)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f'Não foi possivel fazer agendamento: {e}'
        )
    return criar_agendamento

#Consultar Agenda

#Consultar Agendamento especifico
#Excluir Agendamento