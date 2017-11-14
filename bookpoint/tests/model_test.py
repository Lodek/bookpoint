from bookpoint.model.model import Category, Mark, Tag, Base, engine, create_all
from sqlalchemy.orm import sessionmaker
import bookpoint

create_all()

session_db = bookpoint.session_db
