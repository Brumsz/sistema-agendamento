from fastapi import Request,FastAPI,APIRouter,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session,select
from passlib.context import CryptContext
import jwt
from database.models.usuario import *
from database.models.agendamentos import Agendamentos
from database.db import get_session
from config import settings

verificador_JWT = OAuth2PasswordBearer('/usuarios/login')
embaralhador_de_senha = CryptContext(schemes=['bcrypt'], deprecated='auto')

router = APIRouter(prefix="/usuarios",tags=["Usuários"])

#rota de casdastro
@router.post("/cadastro", response_model=UsuariosRead)
def cadastrar_usuario(usuario_dados:UsuariosCreate,session: Session=Depends(get_session)):
    email_existe = session.exec(select(Usuarios).where(Usuarios.email == usuario_dados.email)).first()
    if email_existe:
        raise HTTPException(
            status_code= 400, 
            detail="Este e-mail já está cadastrado."
        )
    usuario_dados.senha = embaralhador_de_senha.hash(usuario_dados.senha)
    novo_usuario = Usuarios(**usuario_dados.model_dump(exclude_unset=True))
    try:
        session.add(novo_usuario)
        session.commit()
        session.refresh(novo_usuario)
    except Exception as e:
        return {'Error': f'Usuario não foi cadastrado no banco de dados, erro: {e}'}
    return novo_usuario

#sistema de login
@router.post('/login')
def fazer_login(form_data:OAuth2PasswordRequestForm = Depends(),session:Session = Depends(get_session)):
    email_existe = session.exec(select(Usuarios).where(Usuarios.email == form_data.username)).first()
    if not email_existe:
        raise HTTPException(
            status_code= 400, 
            detail="Este e-mail não foi cadastrado."
        ) 
    
    senha_discriptografada = embaralhador_de_senha.verify(form_data.password,email_existe.senha)
    if not senha_discriptografada:
        raise HTTPException(
            status_code= 400, 
            detail="A senha esta incorreta"
        )
    payload = {
    "id_usuario": email_existe.id_usuario
    }
    try:
        token = jwt.encode(payload,settings.CHAVE_SECRETA,settings.ALGORITMO)   
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code= 400, 
            detail=f"Erro ao gerar token: {e}"
        )




#rota de consulta de cadastros
@router.get('/',response_model=list[UsuariosRead])
def mostrar_usuarios(session: Session = Depends(get_session)):
    try:
        usuarios = session.exec(select(Usuarios)).all()
    except Exception as e:
        raise e(
            status_code= 400, 
            detail="Não foi possivel buscar os usuarios"
        )
    return usuarios

#consultar unico usuario
@router.get('/{id_usuario}',response_model=UsuariosRead)
def achar_usuario_por_id(id_usuario:int, session: Session = Depends(get_session)):
    usuario_achado = session.exec(select(Usuarios).where(Usuarios.id_usuario == id_usuario)).first()
    if not usuario_achado:
        raise HTTPException(
            status_code= 404, 
            detail=f"Usuario com id {id_usuario} não encontrado."
        )
    return usuario_achado

#deletar usuario
@router.delete('/deletar',response_model=UsuariosRead)
def deletar_usuario(session: Session = Depends(get_session), token:str = Depends(verificador_JWT)):
    try:
        token_descriptografado = jwt.decode(token,settings.CHAVE_SECRETA,algorithms=[settings.ALGORITMO])
    except Exception as e:
        raise HTTPException(
            status_code= 401,
            detail='Token invalido'
        )
    id_encontrado = token_descriptografado['id_usuario']

    usuario_achado = session.exec(select(Usuarios).where(Usuarios.id_usuario == id_encontrado)).first()
    if not usuario_achado:
        raise HTTPException(
            status_code= 404, 
            detail=f"Usuario com id {id_encontrado} não encontrado."
        )
    
    possui_agendamentos = session.exec(select(Agendamentos).where(Agendamentos.id_usuario == usuario_achado.id_usuario)).first()
    if possui_agendamentos:
        try:
            lista_agendamentos_do_usuario = session.exec(select(Agendamentos).where(Agendamentos.id_usuario == usuario_achado.id_usuario)).all()
            for agendamento in lista_agendamentos_do_usuario: session.delete(agendamento)
            session.commit()
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f'Não foi possivel excluir os agendamentos: {e}'
            )
    try:
        session.delete(usuario_achado)
        session.commit()
    except Exception as e:
        raise HTTPException(
            status_code= 400, 
            detail=f"Erro ao excluir usuario"
        )

#atualizar usuario
@router.put('/',response_model=UsuariosRead)
def atualizar_usuario(usuario_dados:UsuariosCreate, session: Session = Depends(get_session),token:str = Depends(verificador_JWT)):
    try:
        token_descriptografado = jwt.decode(token,settings.CHAVE_SECRETA,algorithms=[settings.ALGORITMO])
    except Exception as e:
        raise HTTPException(
            status_code= 401,
            detail='Token invalido'
        )
    id_encontrado = token_descriptografado['id_usuario']

    usuario_achado = session.exec(select(Usuarios).where(Usuarios.id_usuario == id_encontrado)).first()
    if not usuario_achado:
        raise HTTPException(
            status_code= 404, 
            detail=f"Usuario com id {id_encontrado} não encontrado."
        )
    
    novas_informacoes = usuario_dados.model_dump(exclude_unset=True)

    usuario_achado.sqlmodel_update(novas_informacoes)
    
    try:
        session.add(usuario_achado)
        session.commit()
        session.refresh(usuario_achado)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao tentar atualizar usuario: {e}"
        )
    
    return usuario_achado