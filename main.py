from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import mysql.connector
import os

app = FastAPI(title="API ROES Local")

# Configuración de tu DB Local (luego cambiaremos esto a Railway)
#db_config = {
#    'host': '127.0.0.1',
#    'user': 'root',
#    'password': 'Paco8401',
#    'database': 'helpdesk',
#    'port': 3307
#}
# Esto lee las variables que configuraremos en el panel de Railway
db_config = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Paco8401'),
    'database': os.getenv('DB_NAME', 'helpdesk'),
    'port': int(os.getenv('DB_PORT', 3307))
}

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@app.post("/login")
def login(request: LoginRequest):
    try:
        # Imprimimos los valores (sin el password por seguridad) para ver qué está leyendo Railway
        #print(f"DEBUG: Conectando a {os.getenv('DB_HOST')} en el puerto {os.getenv('DB_PORT')}")
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        # Validación de usuario en tabla AUTORIZADOS
        query = "SELECT * FROM AUTORIZADOS WHERE autorizado_email = %s AND autorizado_password = %s"
        cursor.execute(query, (request.email, request.password))
        user = cursor.fetchone()
        
        if user:
            return {"status": "success", "message": "Bienvenido"}
        else:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()