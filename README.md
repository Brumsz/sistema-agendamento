# 📅 Sistema de Agendamento

API REST para agendar horários, com cadastro de usuários e login por JWT. Cada usuário só altera ou cancela os próprios agendamentos, e um horário (data e hora) não pode ser reservado duas vezes.

## ✨ Funcionalidades

- Cadastro de usuário com senha criptografada (bcrypt) e e-mail único
- Login (OAuth2 password flow) que devolve um token JWT
- Criação de agendamentos com data e hora, vinculados ao usuário do token
- Bloqueio de horário já reservado por outro usuário
- Consulta, atualização e exclusão de agendamentos (somente do próprio dono, via token)
- Atualização e exclusão da própria conta (a exclusão remove também os agendamentos do usuário)
- Documentação interativa gerada automaticamente pelo FastAPI (Swagger)

## 🛠️ Tecnologias

Python · FastAPI · SQLModel · PostgreSQL · JWT (PyJWT) · passlib (bcrypt) · pydantic-settings

## 📁 Estrutura do projeto

```
sistema-agendamento/
├── app/
│   ├── main.py                  # Criação da aplicação e registro das rotas
│   └── routes/
│       ├── rotas_usuario.py     # Cadastro, login, consulta, atualização e exclusão de usuário
│       └── rotas_agendamentos.py# Agendar, consultar, atualizar e excluir agendamentos
├── database/
│   ├── db.py                    # Engine, sessão e criação das tabelas
│   └── models/
│       ├── usuario.py           # Modelos de usuário
│       └── agendamentos.py      # Modelos de agendamento
└── config.py                    # Configurações lidas do arquivo .env
```

## 🔌 Endpoints

| Método | Rota | Descrição | Autenticação |
|---|---|---|---|
| POST | `/usuarios/cadastro` | Cria um novo usuário | Não |
| POST | `/usuarios/login` | Gera o token JWT | Não |
| GET | `/usuarios/` | Lista usuários | Não |
| GET | `/usuarios/{id_usuario}` | Consulta um usuário | Não |
| PUT | `/usuarios/` | Atualiza o usuário do token | Sim |
| DELETE | `/usuarios/deletar` | Exclui o usuário do token e seus agendamentos | Sim |
| POST | `/agendamentos/agendar` | Cria um agendamento | Sim |
| GET | `/agendamentos/` | Lista agendamentos | Não |
| GET | `/agendamentos/{id_agendamentos}` | Consulta um agendamento | Não |
| PUT | `/agendamentos/{id_agendamentos}` | Atualiza um agendamento seu | Sim |
| DELETE | `/agendamentos/{id_agendamentos}` | Exclui um agendamento seu | Sim |

## 🚀 Como instalar e rodar

### 1. Clone o repositório

```bash
git clone https://github.com/Brumsz/sistema-agendamento.git
cd sistema-agendamento
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install fastapi uvicorn sqlmodel pydantic-settings pyjwt "passlib[bcrypt]" psycopg2-binary python-multipart
```

### 4. Configure o banco e as variáveis de ambiente

Crie um banco PostgreSQL e um arquivo `.env` na raiz do projeto:

```env
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=agendamento
CHAVE_SECRETA=uma-chave-longa-e-aleatoria
ALGORITMO=HS256
```

### 5. Crie as tabelas

```bash
python -c "from database.db import criar_tabelas; criar_tabelas()"
```

### 6. Inicie o servidor

```bash
uvicorn app.main:app --reload
```

A API estará em `http://127.0.0.1:8000/` e a documentação interativa em `http://127.0.0.1:8000/docs`.

## 🧪 Exemplo de uso

```bash
# 1. Criar usuário
curl -X POST http://127.0.0.1:8000/usuarios/cadastro \
  -H "Content-Type: application/json" \
  -d '{"nome": "João", "email": "joao@email.com", "senha": "senha-forte-123"}'

# 2. Fazer login (o campo "username" recebe o e-mail)
curl -X POST http://127.0.0.1:8000/usuarios/login \
  -d "username=joao@email.com&password=senha-forte-123"

# 3. Agendar um horário (use o access_token do passo 2)
curl -X POST http://127.0.0.1:8000/agendamentos/agendar \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": "2026-12-10", "hora": "14:00:00", "id_usuario": 1}'
```

O `id_usuario` enviado no corpo é substituído pelo id contido no token.

## 📌 Próximos passos

- Exigir autenticação nas rotas de consulta de usuários e agendamentos
- Usar o token também para limitar a leitura aos próprios dados
- Notificações assíncronas de lembrete
- Testes automatizados com pytest

Desenvolvido por João
