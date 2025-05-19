from sqlalchemy.orm import Session
from models import Question,QuestionSet
from schemas import QuestionCreate
from typing import List, Optional

def create_question(db: Session, question: QuestionCreate) -> Question:
    db_question = Question(
        text=question.text,
        max_score=question.max_score
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def get_question(db: Session, question_id: int) -> Optional[Question]:
    return db.query(Question).filter(Question.id == question_id).first()

def get_questions(db: Session, skip: int = 0, limit: int = 100) -> List[Question]:
    return db.query(Question).offset(skip).limit(limit).all()

def get_questions_by_question_set(db: Session, question_set_id: int) -> List[Question]:
    return (
        db.query(Question)
        .join(Question.question_sets)  # join through the secondary table
        .filter(
            QuestionSet.id == question_set_id,
            Question.option_sets.any()  # ensure it has at least one option set
        )
        .all()
    )