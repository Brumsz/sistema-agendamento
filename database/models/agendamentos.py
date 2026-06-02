from sqlmodel import SQLModel,Field
from datetime import date,time

class AgendamentosBase(SQLModel):
    data:date
    hora:time

class AgendamentosCreate(AgendamentosBase):
    id_usuario:int = Field(foreign_key="usuarios.id_usuario")

class Agendamentos(AgendamentosBase,table=True):
    id_agendamentos:int | None = Field(default=None,primary_key=True)
    id_usuario:int = Field(foreign_key="usuarios.id_usuario")

class AgendamentosRead(AgendamentosBase):
    id_agendamentos:int 
    id_usuario:int

