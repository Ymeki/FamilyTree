from sqlalchemy import Column, String, Integer, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(Date, nullable=False)

class FamilyTree(Base):
    __tablename__ = 'family_trees'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    creator_id = Column(String, ForeignKey('users.id'), nullable=False)
    visibility = Column(String, nullable=False)  # ENUM: 'public' or 'private'
    invite_code = Column(String, unique=True, nullable=True)
    created_at = Column(Date, nullable=False)

    creator = relationship("User", back_populates="family_trees")

class TreeMember(Base):
    __tablename__ = 'tree_members'

    id = Column(String, primary_key=True)
    tree_id = Column(String, ForeignKey('family_trees.id'), nullable=False)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=True)  # ENUM: 'male', 'female', etc.
    birth_date = Column(Date, nullable=True)
    death_date = Column(Date, nullable=True)
    bio = Column(String, nullable=True)
    custom_data = Column(JSON, nullable=True)
    father_id = Column(String, ForeignKey('tree_members.id'), nullable=True)
    mother_id = Column(String, ForeignKey('tree_members.id'), nullable=True)
    created_by = Column(String, ForeignKey('users.id'), nullable=False)

    tree = relationship("FamilyTree", back_populates="members")
    father = relationship("TreeMember", remote_side=[id], backref="children_father")
    mother = relationship("TreeMember", remote_side=[id], backref="children_mother")

class TreeRole(Base):
    __tablename__ = 'tree_roles'

    id = Column(String, primary_key=True)
    tree_id = Column(String, ForeignKey('family_trees.id'), nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    role = Column(String, nullable=False)  # ENUM: 'owner', 'manager', 'member'

class MemberAsset(Base):
    __tablename__ = 'member_assets'

    id = Column(String, primary_key=True)
    member_id = Column(String, ForeignKey('tree_members.id'), nullable=False)
    url = Column(String, nullable=False)
    type = Column(String, nullable=False)  # ENUM: 'image', 'doc'
    caption = Column(String, nullable=True)