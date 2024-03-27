from fastapi import FastAPI, HTTPException
import mysql.connector

# MySQL 연결 정보 설정
MYSQL_HOST = "localhost"
MYSQL_USER = "username"
MYSQL_PASSWORD = "password"
MYSQL_DATABASE = "dbname"

# FastAPI 앱 생성
app = FastAPI()

# MySQL 연결 설정
conn = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)
cursor = conn.cursor(dictionary=True)

# 사용자 조회 엔드포인트
@app.get("/users/{user_id}")
def read_user(user_id: int):
    # MySQL SELECT 쿼리 실행
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user