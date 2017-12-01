# Import installed packages
from sqlalchemy import Table, Column, Integer, ForeignKey

# Import app code
from app.core.database import Base

groups_admin_users = Table('groups_admin_users', Base.metadata,
                           Column('user_id', Integer, ForeignKey('user.id')),
                           Column('group_id', Integer, ForeignKey('group.id')))
