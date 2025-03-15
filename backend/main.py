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
from fastapi.staticfiles import StaticFiles
app = FastAPI()
from fastapi import Form
from fastapi import Form, File, UploadFile
from fastapi.responses import FileResponse
from typing import List
import json
import sendgrid
from fastapi import Depends
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
import uuid
from fastapi import BackgroundTasks
from werkzeug.utils import secure_filename

load_dotenv()

# Create uploads directory and its subdirectories
UPLOAD_DIR = "uploads"
AVATARS_DIR = os.path.join(UPLOAD_DIR, "avatars")
os.makedirs(AVATARS_DIR, exist_ok=True)

# Mount the uploads directory for static file serving
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Environment variables
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "mysql://root:@localhost/cafe_preorder")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8080")

# Database configuration
try:
    # Parse DATABASE_URL
    if DATABASE_URL.startswith('mysql://'):
        db_parts = DATABASE_URL.replace('mysql://', '').split('/')
        db_name = db_parts[1]
        db_user_pass_host = db_parts[0].split('@')
        db_host = db_user_pass_host[1] if len(db_user_pass_host) > 1 else 'localhost'
        if '@' in DATABASE_URL:
            db_user_pass = db_user_pass_host[0].split(':')
            db_user = db_user_pass[0]
            db_pass = db_user_pass[1] if len(db_user_pass) > 1 else ''
        else:
            db_user = 'root'
            db_pass = ''
    
    db_config = {
        'host': db_host,
        'user': db_user,
        'password': db_pass,
        'database': db_name
    }
except Exception as e:
    print(f"Error parsing DATABASE_URL: {e}")
    # Fallback to default configuration
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'cafe_preorder'
    }

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Debugging: print values to check if they are loaded correctly.
print(f"SMTP_SERVER: {SMTP_SERVER}, SMTP_PORT: {SMTP_PORT}, SMTP_USER: {SMTP_USER}, FROM_EMAIL: {FROM_EMAIL}")
print(f"Database Config: {db_config}")
ALGORITHM = "HS256"

app = FastAPI()

# Create uploads directory and its subdirectories
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



@app.post("/check-username")
async def check_username(request: dict):
    username = request.get("username")
    
    # Connect to the database and check if the username already exists
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()
    cursor.close()
    connection.close()

    if existing_user:
        return {"exists": True}  # Username already taken
    else:
        return {"exists": False}  # Username is available


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
    avatar_path = os.path.join(AVATARS_DIR, avatar_filename)
    
    try:
        with open(avatar_path, "wb") as file:
            shutil.copyfileobj(avatar.file, file)  # Save the uploaded file to the server
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error uploading avatar")

    # Return the URL to access the uploaded avatar
    avatar_url = f"/uploads/avatars/{avatar_filename}"
    
    return {"message": "Avatar uploaded successfully", "avatar_url": avatar_url}


@app.get("/uploads/avatars/{filename}")
async def get_avatar(filename: str):
    file_path = os.path.join(AVATARS_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Avatar not found")


class OrderStatusUpdate(BaseModel):
    status: str  # Expecting a JSON body with "status"


class OrderItem(BaseModel):
    name: str
    quantity: int
    price: float
    image: Optional[str] = None  # Add image field with default None


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

    try:
        # Start a transaction
        connection.start_transaction()

        # Find the highest existing order_id
        cursor.execute("SELECT MAX(id) FROM orders")
        result = cursor.fetchone()

        last_order_id = result[0] if result[0] else 0
        new_order_id = last_order_id + 1 if last_order_id < 999 else 1  # Reset to 1 when it reaches 999

        # Ensure the order ID is always 3 digits (001, 002, etc.)
        formatted_order_id = f"{new_order_id:03d}"

        # Prepare the order items as JSON
        try:
            items_json = json.dumps([{
                "name": item.name,
                "quantity": item.quantity,
                "price": item.price,
                "image": item.image if hasattr(item, 'image') else None  # Include image path if it exists
            } for item in order.items])
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error processing items: " + str(e))

        # Insert the new order into the database
        cursor.execute(
            "INSERT INTO orders (id, customer_name, items, status) VALUES (%s, %s, %s, %s)",
            (formatted_order_id, order.customer_name, items_json, order.status)
        )

        # Commit the transaction
        connection.commit()

        return {"message": "Order created successfully", "order_id": formatted_order_id}

    except Exception as e:
        # Rollback the transaction in case of an error
        connection.rollback()
        raise HTTPException(status_code=500, detail="Error creating order: " + str(e))

    finally:
        cursor.close()
        connection.close()
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

# Item Management Endpoints
@app.get('/api/items')
async def get_items():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        cursor.close()
        connection.close()
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/api/items')
async def add_item(name: str = Form(...), price: float = Form(...), category: str = Form(None), image: UploadFile = File(...)):
    try:
        # Save image file
        filename = secure_filename(image.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        
        # Ensure upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        image_path = f"/uploads/avatars/{filename}"
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO items (name, price, image, category) VALUES (%s, %s, %s, %s)",
            (name, price, image_path, category)
        )
        
        # Get the ID of the newly inserted item
        item_id = cursor.lastrowid
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"message": "Item added successfully", "image_path": image_path, "id": item_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put('/api/items/{item_id}')
async def update_item(
    item_id: int,
    name: str = Form(...),
    price: float = Form(...),
    category: str = Form(None),
    image: UploadFile = File(None)
):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        if image:
            # Save new image
            filename = secure_filename(image.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            file_path = os.path.join(UPLOAD_DIR, filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            
            image_path = f"/uploads/avatars/{filename}"
            
            # Delete old image if exists
            cursor.execute("SELECT image FROM items WHERE id = %s", (item_id,))
            old_image = cursor.fetchone()
            if old_image and old_image[0]:
                old_path = os.path.join(UPLOAD_DIR, os.path.basename(old_image[0]))
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            cursor.execute(
                "UPDATE items SET name = %s, price = %s, category = %s, image = %s WHERE id = %s",
                (name, price, category, image_path, item_id)
            )
        else:
            cursor.execute(
                "UPDATE items SET name = %s, price = %s, category = %s WHERE id = %s",
                (name, price, category, item_id)
            )
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"message": "Item updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete('/api/items/{item_id}')
async def delete_item(item_id: int):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Get the image path before deleting
        cursor.execute("SELECT image FROM items WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        
        if item and item[0]:
            # Remove the image file
            image_path = os.path.join(UPLOAD_DIR, os.path.basename(item[0]))
            if os.path.exists(image_path):
                os.remove(image_path)
        
        cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"message": "Item deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Category Management Endpoints
@app.get('/api/categories')
async def get_categories():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name, type, icon, created_at FROM categories ORDER BY name")
        categories = cursor.fetchall()
        cursor.close()
        connection.close()
        return {"categories": categories}
    except Exception as e:
        print(f"Error getting categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to get categories")

@app.post('/api/categories')
async def add_category(
    name: str = Form(...),
    type: str = Form(...),
    icon: str = Form(...)
):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Check if category already exists
        cursor.execute("SELECT id FROM categories WHERE name = %s", (name,))
        if cursor.fetchone():
            cursor.close()
            raise HTTPException(status_code=400, detail="Category already exists")
        
        # Validate type
        if type not in ['drinks', 'food']:
            cursor.close()
            raise HTTPException(status_code=400, detail="Invalid category type")
        
        # Insert new category
        cursor.execute(
            "INSERT INTO categories (name, type, icon) VALUES (%s, %s, %s)",
            (name, type, icon)
        )
        connection.commit()
        
        new_category_id = cursor.lastrowid
        cursor.close()
        
        return {
            "id": new_category_id,
            "name": name,
            "type": type,
            "icon": icon,
            "message": "Category added successfully"
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error adding category: {e}")
        raise HTTPException(status_code=500, detail="Failed to add category")

@app.delete('/api/categories/{category_id}')
async def delete_category(category_id: int):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Check if category exists
        cursor.execute("SELECT id FROM categories WHERE id = %s", (category_id,))
        if not cursor.fetchone():
            cursor.close()
            raise HTTPException(status_code=404, detail="Category not found")
        
        # Check if category is in use
        cursor.execute("SELECT id FROM items WHERE category = (SELECT name FROM categories WHERE id = %s)", (category_id,))
        if cursor.fetchone():
            cursor.close()
            raise HTTPException(status_code=400, detail="Cannot delete category that has items")
        
        # Delete category
        cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
        connection.commit()
        cursor.close()
        
        return {"message": "Category deleted successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error deleting category: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete category")

@app.put('/api/categories/{category_id}')
async def update_category(
    category_id: int,
    name: str = Form(...),
    type: str = Form(...),
    icon: str = Form(...)
):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Check if category exists
        cursor.execute("SELECT name FROM categories WHERE id = %s", (category_id,))
        category = cursor.fetchone()
        if not category:
            cursor.close()
            raise HTTPException(status_code=404, detail="Category not found")
            
        old_name = category[0]
        
        # Check if new name already exists (excluding current category)
        cursor.execute("SELECT id FROM categories WHERE name = %s AND id != %s", (name, category_id))
        if cursor.fetchone():
            cursor.close()
            raise HTTPException(status_code=400, detail="Category name already exists")
        
        # Validate type
        if type not in ['drinks', 'food']:
            cursor.close()
            raise HTTPException(status_code=400, detail="Invalid category type")
        
        # Update category
        cursor.execute(
            "UPDATE categories SET name = %s, type = %s, icon = %s WHERE id = %s",
            (name, type, icon, category_id)
        )
        
        # Update items with old category name
        cursor.execute(
            "UPDATE items SET category = %s WHERE category = %s",
            (name, old_name)
        )
        
        connection.commit()
        cursor.close()
        
        return {
            "id": category_id,
            "name": name,
            "type": type,
            "icon": icon,
            "message": "Category updated successfully"
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error updating category: {e}")
        raise HTTPException(status_code=500, detail="Failed to update category")

# Database connection function
def get_db_connection():
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