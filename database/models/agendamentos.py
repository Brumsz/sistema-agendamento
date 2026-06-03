from sqlmodel import SQLModel,Field,Relationship
from datetime import date,time
from database.models.usuario import Usuarios,UsuariosRead
class AgendamentosBase(SQLModel):
    data:date
    hora:time

class AgendamentosCreate(AgendamentosBase):
    id_usuario:int = Field(foreign_key="usuarios.id_usuario")

class Agendamentos(AgendamentosBase,table=True):
    id_agendamentos:int | None = Field(default=None,primary_key=True)
    id_usuario:int = Field(foreign_key="usuarios.id_usuario")
    usuario:None | Usuarios = Relationship() 

class AgendamentosRead(AgendamentosBase):
    id_agendamentos:int 
    id_usuario:int
    usuario:None | UsuariosRead
