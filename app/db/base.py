from sqlalchemy.ext.declarative import declarative_base
from app.models.users import User  # Import all models here

# Create the Base instance
Base = declarative_base()

# Import additional models here as needed
