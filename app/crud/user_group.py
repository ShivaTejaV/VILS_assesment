from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas

def get_user_group(db: Session, id: int) -> Optional[models.UserGroup]:
    return db.query(models.UserGroup).filter(models.UserGroup.id == id).first()

def get_user_groups(db: Session, skip: int = 0, limit: int = 100) -> List[models.UserGroup]:
    return db.query(models.UserGroup).offset(skip).limit(limit).all()

def create_user_group(db: Session, obj_in: schemas.UserGroupCreate) -> models.UserGroup:
    db_obj = models.UserGroup(
        name=obj_in.name,
        assessment_type_id=obj_in.assessment_type_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_user_group(db: Session, db_obj: models.UserGroup, obj_in: schemas.UserGroupCreate) -> models.UserGroup:
    setattr(db_obj, "name", obj_in.name)
    setattr(db_obj, "assessment_type_id", obj_in.assessment_type_id)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_user_group(db: Session, db_obj: models.UserGroup) -> None:
    db.delete(db_obj)
    db.commit()
