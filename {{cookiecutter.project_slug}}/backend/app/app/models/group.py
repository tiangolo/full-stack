# -*- coding: utf-8 -*-

# Import standard library packages
from datetime import datetime
# Import installed packages
from sqlalchemy import (Column, Integer, DateTime, String)
from sqlalchemy.orm import relationship
# Import app code
from ..core.database import Base
from .base_relations import groups_admin_users


class Group(Base):
    # Own properties
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow(), index=True)
    name = Column(String, index=True)
    # Relationships
    users = relationship('User', back_populates='group')
    users_admin = relationship(
        'User', secondary=groups_admin_users, back_populates='groups_admin')
