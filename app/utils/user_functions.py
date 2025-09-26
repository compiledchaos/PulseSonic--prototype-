from app.core.cache import SessionLocal, User_Info


class UserFunctions:
    """Utility class for user management."""

    def __init__(self):
        """Initialize the UserFunctions class."""
        pass

    def check_user_exists(self, username):
        """Check if a user exists in the database."""
        session = SessionLocal()
        user = session.query(User_Info).filter(User_Info.username == username).first()
        session.close()
        return user

    def add_user(self, username, password):
        """Add a new user to the database."""
        session = SessionLocal()
        user = User_Info(username=username, password=password)
        session.add(user)
        session.commit()
        session.close()

    def check_password(self, username: str, password: str) -> bool:
        session = SessionLocal()
        user = session.query(User_Info).filter(User_Info.username == username).first()
        session.close()
        return user.password == password

    def delete_user(self, username: str):
        session = SessionLocal()
        user = session.query(User_Info).filter(User_Info.username == username).first()
        session.delete(user)
        session.commit()
        session.close()
