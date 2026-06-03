from fastapi import APIRouter,Depends,HTTPException
from sqlmodel import Session,select
from database.models.agendamentos import *
from database.models.usuario import *
from database.db import get_session

router = APIRouter(prefix='/agendamentos',tags=['Agendamentos'])

#Agendar
@router.post('/agendar',response_model=AgendamentosRead)
def agendar(dados_agendamento:AgendamentosCreate,session: Session = Depends(get_session)):
    achar_usuario = session.exec(select(Usuarios).where(Usuarios.id_usuario == dados_agendamento.id_usuario)).first()
    if not achar_usuario:
        raise HTTPException(
            status_code=404,
            detail=f'Usuario com id {dados_agendamento.id_usuario} não encontrado.'
        )
    
    horario_ocupado = session.exec(select(Agendamentos).where(Agendamentos.data== dados_agendamento.data).where(Agendamentos.hora == dados_agendamento.hora)).first()
    if horario_ocupado:
        raise HTTPException(
            status_code=400,
            detail='Desculpe, este horário já está reservado por outro usuário.'
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
@router.get('/',response_model=list[AgendamentosRead])
def consultar_agendamentos(session:Session = Depends(get_session)):
    try:
        agendamentos = session.exec(select(Agendamentos)).all()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f'Não foi possivel acessar os agendamentos: {e}'
        )
    return agendamentos

#Consultar Agendamento especifico
@router.get('/{id_agendamentos}',response_model=AgendamentosRead)
def achar_agendamento(id_agendamentos:int,session: Session = Depends(get_session)):
    agendamento_achado = session.exec(select(Agendamentos).where(Agendamentos.id_agendamentos == id_agendamentos)).first()
    if not agendamento_achado:
        raise HTTPException(
            status_code= 404, 
            detail=f"Agendamento com id {id_agendamentos} não encontrado"
        )
    try:
        return agendamento_achado
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail= e
        )
    
#Excluir Agendamento
@router.delete('/{id_agendamentos}')
def deletar_agendamento(id_agendamentos:int,session: Session = Depends(get_session)):
    agendamento_achado = session.exec(select(Agendamentos).where(Agendamentos.id_agendamentos == id_agendamentos)).first()
    if not agendamento_achado:
        raise HTTPException(
            status_code= 404, 
            detail=f"Agendamento com id {id_agendamentos} não encontrado"
        )
    
    try:
        session.delete(agendamento_achado)
        session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail= f'Não foi possivel fazer a exclusão: {e}'
        )

#Mudar agendamento
@router.put('/{id_agendamentos}',response_model=AgendamentosRead)
def atualizar_agendamento(id_agendamentos:int,dados_atualizados_do_agendamento:AgendamentosCreate,session: Session = Depends(get_session)):
    agendamento_achado = session.exec(select(Agendamentos).where(Agendamentos.id_agendamentos == id_agendamentos)).first()
    if not agendamento_achado:
        raise HTTPException(
            status_code= 404, 
            detail=f"Agendamento com id {id_agendamentos} não encontrado"
        )
    
    novas_informacoes = dados_atualizados_do_agendamento.model_dump(exclude_unset=True)
    agendamento_achado.sqlmodel_update(novas_informacoes)

    try:
        session.add(agendamento_achado)
        session.commit()
        session.refresh(agendamento_achado)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f'Não foi possivel atualizar agendamento: {e}'
        )
    return agendamento_achado