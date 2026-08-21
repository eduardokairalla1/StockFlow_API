from app.infraDB.config.connection import db
from app.infraDB.models.users import Users, PermissionType
from app import create_app
import bcrypt
import os

app = create_app()

# Get admin password from environment variable or use default
password = os.getenv("ADMIN_PASSWORD", "admin123")

# Generate a bcrypt hash of the password
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Use the application context to access the database
with app.app_context():
    # Get admin email from environment variable or use default
    email = os.getenv("ADMIN_EMAIL", "admin@email.com")
    
    # Check if an admin user with the specified email already exists
    user = Users.query.filter_by(email=email).first()

    if not user:
        # Create a new admin user if one does not exist
        admin_user = Users(
            name="Admin",
            email=email,
            password_hash=hashed_password,
            permission=PermissionType.ADMIN
        )
        # Add the user to the database and commit the transaction
        db.session.add(admin_user)
        db.session.commit()
        print(f"[OK] Admin user '{email}' created.")
    else:
        # Inform that the user already exists
        print(f"[i] Admin user '{email}' already exists.")
