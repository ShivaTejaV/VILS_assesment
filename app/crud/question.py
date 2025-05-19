from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas

def get_question(db: Session, id: int) -> Optional[models.Question]:
    return db.query(models.Question).filter(models.Question.id == id).first()

def get_questions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Question]:
    return db.query(models.Question).offset(skip).limit(limit).all()

def create_question(db: Session, obj_in: schemas.QuestionCreate) -> models.Question:
    db_obj = models.Question(
        text=obj_in.text,
        max_score=obj_in.max_score
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_question(db: Session, db_obj: models.Question, obj_in: schemas.QuestionCreate) -> models.Question:
    setattr(db_obj, "text", obj_in.text)
    setattr(db_obj, "max_score", obj_in.max_score)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_question(db: Session, db_obj: models.Question) -> None:
    db.delete(db_obj)
    db.commit()
