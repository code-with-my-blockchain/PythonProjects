
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

try:
    from app.db.session import Base, SessionLocal, engine # type: ignore
    from app.models.user import User, UserRole # type: ignore
    from app.core.security import get_password_hash # type: ignore
except ImportError:
   from app.db.session import Base, SessionLocal, engine  # type: ignore
from app.models.user import User, UserRole  # type: ignore
from app.core.security import get_password_hash # type: ignore


def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            print("Admin user already exists.")
        else:
            admin_user = User(
                email="admin@example.com",
                username="admin",
                full_name="System Administrator",
                hashed_password=get_password_hash("admin123"),
                role=UserRole.ADMIN,
                is_superuser=True,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created successfully!")
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
