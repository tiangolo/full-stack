from app.core import config
from app.core.security import pwd_context

from app.models.user import User
from app.models.group import Group


def init_db(db_session):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables uncommenting the next line
    # Base.metadata.create_all(bind=engine)

    group = db_session.query(Group).filter(Group.name == "default").first()
    if not group:
        group = Group(name="default")
        db_session.add(group)

    user = db_session.query(User).filter(User.email == config.FIRST_SUPERUSER).first()
    if not user:
        user = User(
            email=config.FIRST_SUPERUSER,
            password=pwd_context.hash(config.FIRST_SUPERUSER_PASSWORD),
            group=group,
            is_superuser=True,
        )
        user.groups_admin.append(group)

        db_session.add(user)
    db_session.commit()
