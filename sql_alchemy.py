from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import json


class SQL_Alchemy(Node):
    async def run(self) -> str:
        # Create the database engine (SQLite in this case)
        dropdown_test = self.widgets[0]  # {"type": "dropdown", "options": [""]}

        dynamic_options = ["option1", "option2"]
        await self.update_widget_options("dropdown_test", dynamic_options)
        engine = create_engine("sqlite:///example.db", echo=True)

        # Base class for our ORM models
        Base = declarative_base()

        # Define the User model
        class User(Base):
            __tablename__ = "users"

            id = Column(Integer, primary_key=True)
            name = Column(String)
            email = Column(String)

            def __repr__(self):
                return f"<User(name='{self.name}', email='{self.email}')>"

            def to_dict(self):
                return {"id": self.id, "name": self.name, "email": self.email}

        # Create all tables (based on Base subclasses)
        Base.metadata.create_all(engine)

        # Optional: Create a session to interact with the DB
        Session = sessionmaker(bind=engine)
        session = Session()

        # Example insert
        # new_user = User(name="Alice", email="alice@example.com")
        # session.add(new_user)
        # session.commit()

        # result = "hello"
        users = session.query(User).all()
        user_dicts = [user.to_dict() for user in users]
        result = json.dumps(user_dicts)

        return result
