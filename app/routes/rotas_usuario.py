from fastapi import Request,FastAPI,APIRouter,HTTPException,Depends
from sqlmodel import Session,select
from database.models.usuario import *
from database.db import get_session

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
    novo_usuario = Usuarios(**usuario_dados.model_dump(exclude_unset=True))
    try:
        session.add(novo_usuario)
        session.commit()
        session.refresh(novo_usuario)
    except Exception as e:
        return {'Error': f'Usuario não foi cadastrado no banco de dados, erro: {e}'}
    return novo_usuario

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
@router.delete('/{id_usuario}',response_model=UsuariosRead)
def deletar_usuario(id_usuario:int, session: Session = Depends(get_session)):
    usuario_achado = session.exec(select(Usuarios).where(Usuarios.id_usuario == id_usuario)).first()
    if not usuario_achado:
        raise HTTPException(
            status_code= 404, 
            detail=f"Usuario com id {id_usuario} não encontrado."
        )
    try:
        session.delete(usuario_achado)
        session.commit()
    except Exception as e:
        raise e(
            status_code= 400, 
            detail=f"Erro ao excluir usuario"
        )

#atualizar usuario
@router.put('/{id_usuario}',response_model=UsuariosRead)
def atualizar_usuario(id_usuario:int,usuario_dados:UsuariosCreate, session: Session = Depends(get_session)):
    usuario_achado = session.exec(select(Usuarios).where(Usuarios.id_usuario == id_usuario)).first()
    if not usuario_achado:
        raise HTTPException(
            status_code= 404, 
            detail=f"Usuario com id {id_usuario} não encontrado."
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