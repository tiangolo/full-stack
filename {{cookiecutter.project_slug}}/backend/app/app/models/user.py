# -*- coding: utf-8 -*-

# Import standard library packages
from datetime import datetime
# Import installed packages
from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
# Import app code
from ..core.database import Base
from .base_relations import groups_admin_users

# Typings, for autocompletion (VS Code with Python plug-in)
from . import group as group_model  # noqa
from typing import List  # noqa


class User(Base):
    # Own properties
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow(), index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    # Relationships
    group_id = Column(Integer, ForeignKey('group.id'), index=True)
    group = relationship(
        'Group', back_populates='users')  # type: group_model.Group
    # If this user is admin of one or more groups, they will be here
    groups_admin = relationship(
        'Group', secondary=groups_admin_users,
        back_populates='users_admin')  # type: List[group.Group]
