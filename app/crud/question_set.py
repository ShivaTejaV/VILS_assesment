from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas

def get_question_set(db: Session, id: int) -> Optional[models.QuestionSet]:
    return db.query(models.QuestionSet).filter(models.QuestionSet.id == id).first()

def get_question_sets(db: Session, skip: int = 0, limit: int = 100) -> List[models.QuestionSet]:
    return db.query(models.QuestionSet).offset(skip).limit(limit).all()

def create_question_set(db: Session, obj_in: schemas.QuestionSetCreate) -> models.QuestionSet:
    qs = models.QuestionSet(
        assessment_id=obj_in.assessment_id,
        parent_id=obj_in.parent_id,
        version=obj_in.version,
        is_active=obj_in.is_active
    )
    db.add(qs)
    db.commit()
    questions = db.query(models.Question).filter(models.Question.id.in_(obj_in.question_ids)).all()
    qs.questions = questions
    db.commit()
    db.refresh(qs)
    return qs

def update_question_set(db: Session, db_obj: models.QuestionSet, obj_in: schemas.QuestionSetCreate) -> models.QuestionSet:
    setattr(db_obj, "parent_id", obj_in.parent_id)
    setattr(db_obj, "version", obj_in.version)
    setattr(db_obj, "is_active", obj_in.is_active)
    if obj_in.question_ids:
        questions = db.query(models.Question).filter(models.Question.id.in_(obj_in.question_ids)).all()
        db_obj.questions = questions
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_question_set(db: Session, db_obj: models.QuestionSet) -> None:
    db.delete(db_obj)
    db.commit()
