from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas

def get_option(db: Session, id: int) -> Optional[models.Option]:
    return db.query(models.Option).filter(models.Option.id == id).first()

def get_options(db: Session, skip: int = 0, limit: int = 100) -> List[models.Option]:
    return db.query(models.Option).offset(skip).limit(limit).all()

def create_option(db: Session, obj_in: schemas.OptionCreate) -> models.Option:
    db_obj = models.Option(
        text=obj_in.text,
        score=obj_in.score,
        option_set_id=obj_in.option_set_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_option(db: Session, db_obj: models.Option, obj_in: schemas.OptionCreate) -> models.Option:
    setattr(db_obj, "text", obj_in.text)
    setattr(db_obj, "score", obj_in.score)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_option(db: Session, db_obj: models.Option) -> None:
    db.delete(db_obj)
    db.commit()
