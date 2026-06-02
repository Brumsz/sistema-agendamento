from sqlmodel import SQLModel,Field

class UsuariosBase(SQLModel):
    nome:str
    email:str = Field(unique=True)

class UsuariosCreate(UsuariosBase):
    senha:str

class Usuarios(UsuariosBase,table=True):
    id_usuario:int | None = Field(default=None,primary_key=True)
    senha:str

class UsuariosRead(UsuariosBase):
    id_usuario:int

