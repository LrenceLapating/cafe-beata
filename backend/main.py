from fastapi import FastAPI, HTTPException, File, UploadFile, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import Error
import bcrypt  # For password hashing
import shutil
import os
from fastapi import Path, File
from typing import Optional, List
from fastapi.staticfiles import StaticFiles
app = FastAPI()
from fastapi import Form
from fastapi import Form, File, UploadFile
from fastapi.responses import FileResponse
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
    allow_origins=["http://localhost:8080", "https://my-cafe-project.vercel.app/"],  # Add your deployed frontend URL
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
async def request_password_reset(request: ResetPasswordRequest, background_tasks: BackgroundTasks):
    email = request.email

    # Connect to the database and check if the email exists
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user is None:
        raise HTTPException(status_code=400, detail="Email not found")

    # Generate reset token and reset URL
    reset_token = generate_reset_token(email)
    reset_url = f"http://127.0.0.1:8000/reset-password/{reset_token}"

    # Add send_reset_email to background task
    background_tasks.add_task(send_reset_email, email, reset_url)

    # Respond immediately to the client
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
        "database": "cafe_preorderr",  # Your database name
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

    cursor = connection.cursor(dictionary=True)

    try:
        # Check if the order exists
        cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
        order = cursor.fetchone()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Update the status
        cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (status_update.status, order_id))

        # If marking as completed, handle stock reduction
        if status_update.status == "completed":
            items = json.loads(order["items"]) if isinstance(order["items"], str) else order["items"]
            for item in items:
                cursor.execute("SELECT id FROM items WHERE name = %s", (item["name"],))
                item_result = cursor.fetchone()
                if item_result:
                    item_id = item_result["id"]
                    quantity_to_reduce = item["quantity"]
                    cursor.execute(
                        "UPDATE item_stocks SET quantity = quantity - %s WHERE item_id = %s",
                        (quantity_to_reduce, item_id)
                    )

        connection.commit()

        # Broadcast the status update to all connected clients
        await manager.broadcast({
            "type": "order_status_update",
            "order_id": order_id,
            "status": status_update.status,
            "timestamp": datetime.now().isoformat()
        })

        return {"message": f"Order {order_id} marked as {status_update.status}"}

    except Exception as e:
        connection.rollback()
        print(f"Error updating order status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()


# WebSocket Manager for handling multiple connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"New WebSocket connection. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"WebSocket disconnected. Remaining connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected.append(connection)
            except Exception as e:
                print(f"Error broadcasting message: {str(e)}")
                disconnected.append(connection)
        
        # Clean up disconnected connections
        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()

@app.websocket("/ws/orders")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive and wait for any messages
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        manager.disconnect(websocket)

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
        new_order_id = last_order_id + 1 if last_order_id < 999 else 1

        # Ensure the order ID is always 3 digits
        formatted_order_id = f"{new_order_id:03d}"

        # Prepare the order items as JSON
        try:
            items_json = json.dumps([{
                "name": item.name,
                "quantity": item.quantity,
                "price": item.price,
                "image": item.image if hasattr(item, 'image') else None
            } for item in order.items])
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error processing items: " + str(e))

        # Insert the new order
        cursor.execute(
            "INSERT INTO orders (id, customer_name, items, status) VALUES (%s, %s, %s, %s)",
            (formatted_order_id, order.customer_name, items_json, order.status)
        )

        # Commit the transaction
        connection.commit()

        # Create the order object for broadcasting
        order_data = {
            "id": formatted_order_id,
            "customer_name": order.customer_name,
            "items": [item.dict() for item in order.items],
            "status": order.status,
            "created_at": datetime.now().isoformat()
        }

        # Broadcast the new order to all connected clients
        await manager.broadcast({
            "type": "new_order",
            "order": order_data
        })

        return {"message": "Order created successfully", "order_id": formatted_order_id}

    except Exception as e:
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
        
        # Create initial stock record for the item
        cursor.execute(
            "INSERT INTO item_stocks (item_id, quantity, min_stock_level) VALUES (%s, %s, %s)",
            (item_id, 0, 0)  # Default values: 0 quantity and 0 min_stock_level
        )
        
        connection.commit()
        cursor.close()
        connection.close()
        
        # Broadcast menu update
        await manager.broadcast({
            "type": "menu_update",
            "action": "add",
            "item": {
                "id": item_id,
                "name": name,
                "price": price,
                "category": category,
                "image": image_path
            }
        })
        
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
        
        # Broadcast menu update
        await manager.broadcast({
            "type": "menu_update",
            "action": "update",
            "item": {
                "id": item_id,
                "name": name,
                "price": price,
                "category": category,
                "image": image_path if image else None
            }
        })
        
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
        
        # Delete the item's stock record first
        cursor.execute("DELETE FROM item_stocks WHERE item_id = %s", (item_id,))
        
        # Then delete the item
        cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
        connection.commit()
        cursor.close()
        connection.close()
        
        # Broadcast menu update
        await manager.broadcast({
            "type": "menu_update",
            "action": "delete",
            "item_id": item_id
        })
        
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
        
        # Broadcast category update via WebSocket
        await manager.broadcast({
            "type": "category_update",
            "action": "add",
            "category": {
                "id": new_category_id,
                "name": name,
                "type": type,
                "icon": icon
            }
        })
        
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
        cursor.execute("SELECT name FROM categories WHERE id = %s", (category_id,))
        category = cursor.fetchone()
        if not category:
            cursor.close()
            raise HTTPException(status_code=404, detail="Category not found")
        
        category_name = category[0]
        
        # Check if category is in use
        cursor.execute("SELECT id FROM items WHERE category = %s", (category_name,))
        if cursor.fetchone():
            cursor.close()
            raise HTTPException(status_code=400, detail="Cannot delete category that has items")
        
        # Delete category
        cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
        connection.commit()
        cursor.close()
        
        # Broadcast category update via WebSocket
        await manager.broadcast({
            "type": "category_update",
            "action": "delete",
            "category_id": category_id,
            "category_name": category_name
        })
        
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
        
        # Broadcast category update via WebSocket
        await manager.broadcast({
            "type": "category_update",
            "action": "update",
            "category": {
                "id": category_id,
                "name": name,
                "type": type,
                "icon": icon,
                "old_name": old_name
            }
        })
        
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

# Stock Management Models
class StockUpdate(BaseModel):
    action: str  # 'add', 'subtract', or 'set'
    quantity: int
    reason: str

class MinStockLevel(BaseModel):
    min_stock_level: int

# Stock Management Endpoints
@app.get('/api/stocks')
async def get_stocks():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.*, i.name as item_name, i.category 
            FROM item_stocks s 
            JOIN items i ON s.item_id = i.id
        """)
        stocks = cursor.fetchall()
        cursor.close()
        connection.close()
        return {"success": True, "items": stocks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/api/stocks')
async def create_stock_record(request: dict):
    try:
        item_id = request.get("item_id")
        quantity = request.get("quantity", 0)
        min_stock_level = request.get("min_stock_level", 0)
        
        if not item_id:
            raise HTTPException(status_code=400, detail="Item ID is required")
            
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Check if stock record already exists
        cursor.execute("SELECT item_id FROM item_stocks WHERE item_id = %s", (item_id,))
        if cursor.fetchone():
            cursor.close()
            connection.close()
            return {"success": False, "message": "Stock record already exists for this item"}
        
        # Create new stock record
        cursor.execute(
            "INSERT INTO item_stocks (item_id, quantity, min_stock_level) VALUES (%s, %s, %s)",
            (item_id, quantity, min_stock_level)
        )
        
        connection.commit()
        cursor.close()
        connection.close()
        
        # Broadcast stock update
        await manager.broadcast({
            "type": "stock_update",
            "item_id": item_id,
            "new_quantity": quantity,
            "min_stock_level": min_stock_level
        })
        
        return {"success": True, "message": "Stock record created successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put('/api/stocks/{item_id}/update')
async def update_stock(item_id: int, stock_update: StockUpdate):
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # First check if the tables exist
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'cafe_preorderr' 
            AND table_name IN ('item_stocks', 'stock_transactions', 'stock_alerts')
        """)
        tables_count = cursor.fetchone()[0]
        if tables_count < 3:
            raise HTTPException(status_code=500, detail="Required database tables are missing")

        # First get current stock and item details
        cursor.execute("""
            SELECT s.quantity, s.min_stock_level, i.name as item_name, i.category 
            FROM item_stocks s 
            JOIN items i ON s.item_id = i.id 
            WHERE s.item_id = %s
        """, (item_id,))
        stock_result = cursor.fetchone()
        
        if not stock_result:
            raise HTTPException(status_code=404, detail=f"Stock record not found for item_id: {item_id}")
        
        current_quantity = stock_result[0]
        min_stock_level = stock_result[1]
        item_name = stock_result[2]
        category = stock_result[3]
        new_quantity = current_quantity

        print(f"Processing stock update - Action: {stock_update.action}, Current: {current_quantity}, Update: {stock_update.quantity}")

        # Calculate new quantity based on action
        if stock_update.action == "add":
            new_quantity = current_quantity + stock_update.quantity
        elif stock_update.action == "subtract":
            if current_quantity < stock_update.quantity:
                raise HTTPException(status_code=400, detail="Not enough stock")
            new_quantity = current_quantity - stock_update.quantity
        elif stock_update.action == "set":
            new_quantity = stock_update.quantity
        else:
            raise HTTPException(status_code=400, detail=f"Invalid action: {stock_update.action}")

        print(f"New quantity calculated: {new_quantity}")

        # Update stock
        try:
            cursor.execute(
                "UPDATE item_stocks SET quantity = %s WHERE item_id = %s",
                (new_quantity, item_id)
            )
            print(f"Stock updated successfully for item_id: {item_id}")
        except Exception as e:
            print(f"Error updating stock: {str(e)}")
            raise

        # Log transaction
        try:
            cursor.execute(
                """INSERT INTO stock_transactions 
                   (item_id, action, quantity, previous_quantity, new_quantity, reason) 
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (item_id, stock_update.action, stock_update.quantity, current_quantity, new_quantity, stock_update.reason)
            )
            print("Transaction logged successfully")
        except Exception as e:
            print(f"Error logging transaction: {str(e)}")
            # Continue even if logging fails
            pass

        # Check if we need to create an alert
        alert_type = None
        try:
            if new_quantity <= min_stock_level:
                alert_type = "out_of_stock" if new_quantity == 0 else "low_stock"
                cursor.execute(
                    """INSERT INTO stock_alerts (item_id, alert_type, quantity) 
                       VALUES (%s, %s, %s)
                       ON DUPLICATE KEY UPDATE 
                       alert_type = VALUES(alert_type),
                       quantity = VALUES(quantity),
                       created_at = CURRENT_TIMESTAMP""",
                    (item_id, alert_type, new_quantity)
                )
                print(f"Stock alert created: {alert_type}")
        except Exception as e:
            print(f"Error handling stock alert: {str(e)}")
            # Continue even if alert creation fails
            pass

        connection.commit()
        print("Transaction committed successfully")

        # Broadcast stock update via WebSocket
        await manager.broadcast({
            "type": "stock_update",
            "item_id": item_id,
            "item_name": item_name,
            "category": category,
            "new_quantity": new_quantity,
            "min_stock_level": min_stock_level,
            "alert_type": alert_type
        })

        return {"success": True, "new_quantity": new_quantity}
    except HTTPException as he:
        if connection:
            connection.rollback()
        raise he
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Unexpected error in stock update: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Database connection closed")

@app.put('/api/stocks/{item_id}/min-level')
async def update_min_stock_level(item_id: int, min_stock: MinStockLevel):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute(
            "UPDATE item_stocks SET min_stock_level = %s WHERE item_id = %s",
            (min_stock.min_stock_level, item_id)
        )
        
        connection.commit()
        cursor.close()
        connection.close()
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/stocks/alerts')
async def get_stock_alerts():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.*, i.name as item_name, i.category 
            FROM stock_alerts a 
            JOIN items i ON a.item_id = i.id 
            ORDER BY a.created_at DESC
        """)
        alerts = cursor.fetchall()
        cursor.close()
        connection.close()
        return {"success": True, "alerts": alerts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def create_stock_tables():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # Create item_stocks table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS item_stocks (
                item_id INT PRIMARY KEY,
                quantity INT NOT NULL DEFAULT 0,
                min_stock_level INT NOT NULL DEFAULT 0,
                FOREIGN KEY (item_id) REFERENCES items(id)
            )
        """)

        # Create stock_transactions table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                item_id INT NOT NULL,
                action VARCHAR(50) NOT NULL,
                quantity INT NOT NULL,
                previous_quantity INT NOT NULL,
                new_quantity INT NOT NULL,
                reason TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (item_id) REFERENCES items(id)
            )
        """)

        # Create stock_alerts table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_alerts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                item_id INT NOT NULL,
                alert_type VARCHAR(50) NOT NULL,
                quantity INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (item_id) REFERENCES items(id),
                UNIQUE KEY unique_item_alert (item_id)
            )
        """)

        connection.commit()
        print("Stock management tables created successfully")
    except Exception as e:
        print(f"Error creating stock tables: {str(e)}")
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()

# Call create_stock_tables when the application starts
@app.on_event("startup")
async def startup_event():
    create_stock_tables()