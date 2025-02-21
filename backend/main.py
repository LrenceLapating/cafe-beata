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
from typing import List
import json
import sendgrid
from dotenv import load_dotenv
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi.responses import JSONResponse
import smtplib
import jwt
from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, HTTPException, Path



load_dotenv()


SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")
SECRET_KEY = os.getenv("SECRET_KEY")

# Debugging: print values to check if they are loaded correctly.
print(f"SMTP_SERVER: {SMTP_SERVER}, SMTP_PORT: {SMTP_PORT}, SMTP_USER: {SMTP_USER}, FROM_EMAIL: {FROM_EMAIL}")
ALGORITHM = "HS256"

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Make sure this is set to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResetPasswordRequest(BaseModel):
    email: str

class ResetPassword(BaseModel):
    newPassword: str


def generate_reset_token(email: str):
    expiration = datetime.utcnow() + timedelta(hours=1)
    to_encode = {"exp": expiration, "sub": email}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def send_reset_email(to_email, reset_url):
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = 'Password Reset Request'

    body = f'Click the following link to reset your password: {reset_url}'
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.set_debuglevel(1)
        server.connect(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(FROM_EMAIL, to_email, text)
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

import mysql.connector

@app.post("/request-password-reset")
async def request_password_reset(request: ResetPasswordRequest):
    email = request.email

    # Connect to the database and check if the email exists
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user is None:
        raise HTTPException(status_code=400, detail="Email not found")

    # Generate reset token and send reset email
    reset_token = generate_reset_token(email)
    reset_url = f"http://127.0.0.1:8000/reset-password/{reset_token}"
    send_reset_email(email, reset_url)

    return {"message": "Password reset link sent to your email!"}

@app.get("/reset-password/{token}")
async def reset_password_page(token: str):
    """Redirect to frontend reset password page"""
    reset_url = f"http://localhost:8080/reset-password/{token}"  # Make sure this URL matches your frontend route
    return RedirectResponse(url=reset_url)
    

@app.post("/reset-password/{token}")
async def reset_password_with_token(token: str, reset_data: ResetPassword):
    print(f"Received token: {token}")  # Debugging: print received token
    
    try:
        # Decode the token to extract the email
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = decoded_token.get("sub")

        # If no email is found in the token, throw an error
        if not email:
            raise HTTPException(status_code=400, detail="Email not found in token")

        # Check if the token is expired
        if datetime.utcnow() > datetime.utcfromtimestamp(decoded_token["exp"]):
            raise HTTPException(status_code=400, detail="Token expired")

        # Proceed with updating the password in the database
        hashed_new_password = bcrypt.hashpw(reset_data.newPassword.encode('utf-8'), bcrypt.gensalt())

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_new_password, email))
        connection.commit()

        return {"message": "Password reset successfully!"}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    except jwt.PyJWTError as e:  # Correct exception name for PyJWT
        print(f"Error decoding JWT: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid token")






# Database connection function
def get_db_connection():
    db_config = {
        "host": "127.0.0.1",  # Your MySQL host
        "user": "root",        # Your MySQL user
        "password": "Warweapons19",  # Your MySQL password
        "database": "cafe_preorder",  # Your database name
    }

    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

@app.get("/")
async def root():
    return {"message": "FastAPI is running with CORS enabled!"}





UPLOAD_DIR = "uploads/avatars"

# Model for User registration and login (Only email and password for login)
class User(BaseModel):
    email: str
    password: str
    username: str 
# Separate model for login (no secret_answer)
class UserLogin(BaseModel):
    email: str
    password: str  # Only email and password needed for login

# Model for password reset functionality

# Model for User Profile Data
class UserProfile(BaseModel):
    username: str
    email: str
    course: str
    gender: str
    about_me: str

@app.post("/register")
async def register(user: User):
    print(f"Received user data: {user}")  # Debugging: print the received user data
    if not user.email.endswith("@uic.edu.ph"):
        raise HTTPException(status_code=400, detail="Email must be the UIC EMAIL address")

    username = user.username  

    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    existing_user = cursor.fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password before storing
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    # Store the username (no secret_answer)
    cursor.execute("INSERT INTO users (email, password, username) VALUES (%s, %s, %s)", 
                   (user.email, hashed_password, username))  
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

    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    db_user = cursor.fetchone()

    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email")

    stored_password = db_user[2]
    if not bcrypt.checkpw(user.password.encode('utf-8'), stored_password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Incorrect password")

    cursor.close()
    connection.close()

    return {"message": "Login successful", "username": db_user[3]}  # Return the username (assuming it is at index 3)



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
    
    # You would save this URL in the database, assuming you have a users table with an avatar column.
    # Here's a placeholder for saving the avatar URL in your DB (not implemented here)
    
    return {"message": "Avatar uploaded successfully", "avatar_url": avatar_url}


@app.get("/uploads/avatars/{filename}")
async def get_avatar(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Avatar not found")


class OrderStatusUpdate(BaseModel):
    status: str  # Expecting a JSON body with "status"


class OrderItem(BaseModel):
    name: str
    quantity: int
    price: float


class Order(BaseModel):
    customer_name: str
    items: List[OrderItem]  # List of OrderItem objects
    status: str


@app.get("/orders")
async def get_orders(status: Optional[str] = "pending", customer_name: Optional[str] = None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if customer_name:
        cursor.execute("SELECT * FROM orders WHERE customer_name = %s AND status = %s", (customer_name, status))
    else:
        cursor.execute("SELECT * FROM orders WHERE status = %s", (status,))  # Fetch orders by status

    orders = cursor.fetchall()

    for order in orders:
        try:
            if isinstance(order["items"], str):  
                order["items"] = json.loads(order["items"])  
        except json.JSONDecodeError:
            order["items"] = []  

    cursor.close()
    connection.close()

    return {"orders": orders}



@app.put("/orders/{order_id}")
async def update_order_status(order_id: str, status_update: OrderStatusUpdate):
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = connection.cursor()

    # Check if the order exists
    cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    order = cursor.fetchone()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update the status
    cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (status_update.status, order_id))
    connection.commit()

    cursor.close()
    connection.close()

    return {"message": f"Order {order_id} marked as {status_update.status}"}


@app.post("/orders")
async def create_order(order: Order):
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = connection.cursor()

    # Fetch the maximum Order ID from the database
    cursor.execute("SELECT MAX(CAST(id AS UNSIGNED)) FROM orders")
    result = cursor.fetchone()

    # Get the last Order ID as an integer (default to 0 if no orders exist)
    last_order_id = int(result[0]) if result[0] is not None else 0

    # Generate the new Order ID (001-999 loop)
    new_order_id = last_order_id + 1 if last_order_id < 999 else 1

    # Ensure the order ID is stored as a three-digit string (e.g., "001", "045", "999")
    formatted_order_id = f"{new_order_id:03d}"  # Converts 1 → "001", 45 → "045", 999 → "999"

    # Prepare the order items as JSON
    try:
        items_json = json.dumps([{
            "name": item.name,
            "quantity": item.quantity,
            "price": item.price
        } for item in order.items])
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error processing items: " + str(e))

    # Insert the new order with the formatted Order ID
    cursor.execute(
        "INSERT INTO orders (id, customer_name, items, status) VALUES (%s, %s, %s, %s)",
        (formatted_order_id, order.customer_name, items_json, order.status)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return {"message": "Order created successfully", "order_id": formatted_order_id}



@app.get("/orders/{order_id}")
async def get_order_details(order_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    order = cursor.fetchone()
    cursor.close()
    connection.close()

    if order:
        try:
            order["items"] = json.loads(order["items"]) if order["items"] else []
        except json.JSONDecodeError:
            order["items"] = []

        return order
    else:
        raise HTTPException(status_code=404, detail="Order not found")