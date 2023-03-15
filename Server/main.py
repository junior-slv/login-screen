from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector


app = FastAPI()

class User(BaseModel):
    username: str
    password: str
    email: str
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="login-teste"
    )

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/users/")
def create_user(user: User):
    # Criptografar a senha
    hashed_password = hash(user.password)
    
    # Conectar ao banco de dados
    conn = connect_to_database()
    cursor = conn.cursor()
    
    # Inserir os dados do usuário no banco de dados
    query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
    values = (user.username, hashed_password, user.email)
    cursor.execute(query, values)
    
    # Commit e fechar a conexão
    conn.commit()
    conn.close()
    
    # Retornar uma mensagem de sucesso
    return {"message": "User created successfully"}