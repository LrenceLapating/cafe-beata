
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import Error
import bcrypt  # For password hashing
import shutil
import os
from fastapi import Path, File
from typing import Optional
app = FastAPI()
from fastapi import Form
from fastapi import Form, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

UPLOAD_DIR = "uploads/avatars"



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
async def root():
    return {"message": "FastAPI is running with CORS enabled!"}



if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains to access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MySQL Database connection details
db_config = {
    "host": "127.0.0.1",  # Your MySQL host
    "user": "root",        # Your MySQL user (default in XAMPP is root)
    "password": "",        # Your MySQL password (default in XAMPP is empty)
    "database": "cafe_preorder",  # Your database name
}

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None



# Model for User registration and login (Only email and password for login)
class User(BaseModel):
    email: str
    password: str
    secret_answer: str  # Including secret_answer for registration
    username: str 
# Separate model for login (no secret_answer)
class UserLogin(BaseModel):
    email: str
    password: str  # Only email and password needed for login

# Model for password reset functionality
class ResetPassword(BaseModel):
    email: str
    newPassword: str
    secret_answer: str  # The answer to the secret question

# Model for User Profile Data
class UserProfile(BaseModel):
    username: str
    email: str
    course: str
    gender: str
    about_me: str

@app.post("/register")
async def register(user: User):
    # Validate that the email ends with @uic.edu.ph
    if not user.email.endswith("@uic.edu.ph"):
        raise HTTPException(status_code=400, detail="Email must be the UIC EMAIL address")

    # Use the username provided during registration (now from the frontend)
    username = user.username  # Use the username from the request body

    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = connection.cursor()

    # Check if email is already registered
    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    existing_user = cursor.fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    # Insert new user into the database (store hashed password and the actual secret_answer)
    cursor.execute("INSERT INTO users (email, password, secret_answer, username) VALUES (%s, %s, %s, %s)", 
                   (user.email, hashed_password, user.secret_answer, username))  # Store the username automatically
    connection.commit()
    cursor.close()
    connection.close()

    return {"message": "Account created successfully"}


@app.post("/login")
async def login(user: UserLogin):
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = connection.cursor()

    # Check if email exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    db_user = cursor.fetchone()
    
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email ")
    
    # Compare the entered password with the stored hashed password
    stored_password = db_user[2]  # The stored password is at index 2 (third column)
    if not bcrypt.checkpw(user.password.encode('utf-8'), stored_password.encode('utf-8')):  # Hash comparison
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    cursor.close()
    connection.close()

    return {"message": "Login successful"}

@app.post("/reset-password")
async def reset_password(reset_data: ResetPassword):
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = connection.cursor()

    # Check if email exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (reset_data.email,))
    db_user = cursor.fetchone()
    
    if not db_user:
        raise HTTPException(status_code=400, detail="Email not found")

    # Compare the secret answers
    stored_secret_answer = db_user[3].strip().lower()  # Assuming secret_answer is at index 3
    user_secret_answer = reset_data.secret_answer.strip().lower()

    if user_secret_answer != stored_secret_answer:
        raise HTTPException(status_code=400, detail="Incorrect answer to secret question")

    # Hash the new password before updating it
    hashed_new_password = bcrypt.hashpw(reset_data.newPassword.encode('utf-8'), bcrypt.gensalt())

    # Update the password
    cursor.execute("UPDATE users SET password = %s WHERE email = %s", 
                   (hashed_new_password, reset_data.email))  # Store the new password as hashed
    connection.commit()
    cursor.close()
    connection.close()

    return {"message": "Password reset successful"}

@app.get("/profile/{email}")
async def get_profile(email: str):
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = connection.cursor()
    cursor.execute("SELECT id, email, username, course, gender, avatar FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user:
        # Return the avatar path stored in the database
        return {
            "id": user[0],
            "email": user[1],
            "username": user[2],
            "course": user[3],
            "gender": user[4],
            "avatar": user[5] if user[5] else "/assets/default.png"  # Fallback to default if no avatar
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")



@app.put("/profile/{email}")
async def update_profile(
    email: str,
    username: str = Form(...),
    course: str = Form(...),
    gender: str = Form(...),
    avatar: Optional[str] = Form(None)  # Avatar can be a file path or URL
):
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cursor = connection.cursor()

        # Update user profile in the database with the selected avatar (URL or file path)
        cursor.execute(
            """
            UPDATE users
            SET username = %s, course = %s, gender = %s, avatar = %s
            WHERE email = %s
            """,
            (username, course, gender, avatar, email)
        )
        connection.commit()

        return {"message": "Profile updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating profile: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.post("/profile/upload-avatar/{email}")
async def upload_avatar(email: str, avatar: UploadFile = File(...)):
    # Define the file path
    avatar_filename = f"{email}_{avatar.filename}"
    avatar_path = os.path.join(UPLOAD_DIR, avatar_filename)
    
    try:
        with open(avatar_path, "wb") as file:
            shutil.copyfileobj(avatar.file, file)  # Save the uploaded file to the server
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error uploading avatar")

    # Return the URL to access the uploaded avatar
    avatar_url = f"/uploads/avatars/{avatar_filename}"
    
    # You would save this URL in the database, assuming you have a `users` table with an `avatar` column.
    # Here's a placeholder for saving the avatar URL in your DB (not implemented here)
    
    return {"message": "Avatar uploaded successfully", "avatar_url": avatar_url}


@app.get("/uploads/avatars/{filename}")
async def get_avatar(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Avatar not found")


