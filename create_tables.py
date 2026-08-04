"""
Quick script to create all tables.
Run from backend folder:
    python create_tables.py
"""
from app.db.session import engine, Base
from app.models import User, Document, Conversation, Message, AuditLog

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ All tables created successfully!")
