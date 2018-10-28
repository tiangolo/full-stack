from app.core import config
from app.core.security import pwd_context

from app.db.utils import (
    get_role_by_name,
    create_role,
    get_user_by_username,
    create_user,
    assign_role_to_user,
)
from app.core.security import get_password_hash

from app.models.user import User
from app.models.role import Role


def init_db(db_session):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables uncommenting the next line
    # Base.metadata.create_all(bind=engine)

    role = get_role_by_name("default", db_session)
    if not role:
        role = create_role("default", db_session)

    user = get_user_by_username(config.FIRST_SUPERUSER, db_session)
    if not user:
        user = create_user(
            db_session,
            config.FIRST_SUPERUSER,
            config.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        assign_role_to_user(role, user, db_session)
