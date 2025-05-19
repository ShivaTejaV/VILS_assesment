from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas

def get_option_set(db: Session, id: int) -> Optional[models.OptionSet]:
    return db.query(models.OptionSet).filter(models.OptionSet.id == id).first()

def get_option_sets(db: Session, skip: int = 0, limit: int = 100) -> List[models.OptionSet]:
    return db.query(models.OptionSet).offset(skip).limit(limit).all()

def create_option_set(db: Session, obj_in: schemas.OptionSetCreate) -> models.OptionSet:
    os = models.OptionSet(
        question_id=obj_in.question_id,
        version=obj_in.version,
        is_active=obj_in.is_active
    )
    db.add(os)
    db.commit()
    for opt in obj_in.options:
        db.add(models.Option(
            text=opt.text,
            score=opt.score,
            option_set_id=os.id
        ))
    db.commit()
    db.refresh(os)
    return os

def update_option_set(db: Session, db_obj: models.OptionSet, obj_in: schemas.OptionSetCreate) -> models.OptionSet:
    setattr(db_obj, "question_id", obj_in.question_id)
    setattr(db_obj, "version", obj_in.version)
    setattr(db_obj, "is_active", obj_in.is_active)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_option_set(db: Session, db_obj: models.OptionSet) -> None:
    db.delete(db_obj)
    db.commit()
