from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class FamilyTreeBase(BaseModel):
    name: str
    visibility: str  # 'public' or 'private'
    invite_code: Optional[str] = None

class FamilyTreeCreate(FamilyTreeBase):
    pass

class FamilyTree(FamilyTreeBase):
    id: UUID
    creator_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class TreeMemberBase(BaseModel):
    name: str
    gender: str
    birth_date: Optional[datetime] = None
    death_date: Optional[datetime] = None
    bio: Optional[str] = None
    custom_data: Optional[dict] = None

class TreeMemberCreate(TreeMemberBase):
    father_id: Optional[UUID] = None
    mother_id: Optional[UUID] = None

class TreeMember(TreeMemberBase):
    id: UUID
    tree_id: UUID
    created_by: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class TreeRoleBase(BaseModel):
    role: str  # 'owner', 'manager', or 'member'

class TreeRoleCreate(TreeRoleBase):
    pass

class TreeRole(TreeRoleBase):
    id: UUID
    tree_id: UUID
    user_id: UUID

    class Config:
        orm_mode = True

class MemberAssetBase(BaseModel):
    url: str
    type: str  # 'image' or 'doc'
    caption: Optional[str] = None

class MemberAssetCreate(MemberAssetBase):
    pass

class MemberAsset(MemberAssetBase):
    id: UUID
    member_id: UUID

    class Config:
        orm_mode = True