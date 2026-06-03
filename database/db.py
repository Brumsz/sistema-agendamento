from sqlmodel import SQLModel,create_engine,Session
from database.models.agendamentos import Agendamentos
from database.models.usuario import Usuarios
from config import settings

#datebase_url herdada do env
DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL,echo=True)

def criar_tabelas():
    SQLModel.metadata.create_all(engine)
    print('tabelas criadas')

#essa função abre uma sessão no banco de dados, e sera usado em outras partes do codigo para acessar o banco de dados
def get_session():
    with Session(engine) as session:
        yield session



