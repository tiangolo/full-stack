from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from . import config
from .security import pwd_context

engine = create_engine(
    f'postgresql://postgres:{config.POSTGRES_PASSWORD}@db/app',
    convert_unicode=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=Base)
Base.query = db_session.query_property()

# Import all the models, so that Base has them before being
# imported by Alembic or used by init_db()
from app.models.user import User
from app.models.group import Group

def init_db():
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create the tables uncommenting the next line
    # Base.metadata.create_all(bind=engine)

    group = db_session.query(Group).filter(Group.name == 'default').first()
    if not group:
        group = Group(name='default')
        db_session.add(group)

    user = db_session.query(User).filter(
        User.email == config.FIRST_SUPERUSER).first()
    if not user:
        user = User(
            email=config.FIRST_SUPERUSER,
            password=pwd_context.hash(config.FIRST_SUPERUSER_PASSWORD),
            group=group,
            is_superuser=True)
        user.groups_admin.append(group)

        db_session.add(user)
    db_session.commit()
