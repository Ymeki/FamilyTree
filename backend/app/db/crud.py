def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_family_tree(db: Session, family_tree: FamilyTreeCreate, creator_id: int):
    db_family_tree = FamilyTree(**family_tree.dict(), creator_id=creator_id)
    db.add(db_family_tree)
    db.commit()
    db.refresh(db_family_tree)
    return db_family_tree

def get_family_tree(db: Session, tree_id: int):
    return db.query(FamilyTree).filter(FamilyTree.id == tree_id).first()

def get_family_trees(db: Session, creator_id: int):
    return db.query(FamilyTree).filter(FamilyTree.creator_id == creator_id).all()

def add_member_to_tree(db: Session, tree_id: int, member: TreeMemberCreate):
    db_member = TreeMember(**member.dict(), tree_id=tree_id)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_tree_members(db: Session, tree_id: int):
    return db.query(TreeMember).filter(TreeMember.tree_id == tree_id).all()

def get_member(db: Session, member_id: int):
    return db.query(TreeMember).filter(TreeMember.id == member_id).first()