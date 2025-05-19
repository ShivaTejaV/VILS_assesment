from sqlalchemy.orm import Session
from models import QuestionSet, Question
from schemas import QuestionSetCreate
from typing import List, Optional

# ─── Create QuestionSet with auto versioning ─────────────────

def create_question_set(db: Session, data: QuestionSetCreate) -> QuestionSet:
    # Get latest version for the given assessment
    last_qs = (
        db.query(QuestionSet)
        .filter(QuestionSet.assessment_id == data.assessment_id)
        .order_by(QuestionSet.version.desc())
        .first()
    )
    new_version = (last_qs.version + 1) if last_qs else 1

    db_qs = QuestionSet(
        assessment_id=data.assessment_id,
        version=new_version,
        is_active=False  # Always false on creation
    )

    db.add(db_qs)
    db.commit()
    db.refresh(db_qs)

    # Link questions
    questions = db.query(Question).filter(Question.id.in_(data.question_ids)).all()
    db_qs.questions.extend(questions)

    db.commit()
    db.refresh(db_qs)
    return db_qs

# ─── Get QuestionSet by ID ───────────────────────────────────

def get_question_set(db: Session, question_set_id: int) -> Optional[QuestionSet]:
    return db.query(QuestionSet).filter(QuestionSet.id == question_set_id).first()

# ─── Get all QuestionSets by assessment ID ───────────────────

def get_question_sets_by_assessment(db: Session, assessment_id: int) -> List[QuestionSet]:
    return (
        db.query(QuestionSet)
        .filter(QuestionSet.assessment_id == assessment_id)
        .order_by(QuestionSet.version.desc())
        .all()
    )

# ─── Get active QuestionSet by assessment ID ─────────────────

def get_active_question_set_by_assessment(db: Session, assessment_id: int) -> Optional[QuestionSet]:
    return (
        db.query(QuestionSet)
        .filter(
            QuestionSet.assessment_id == assessment_id,
            QuestionSet.is_active == True
        )
        .first()
    )

# ─── Activate a specific QuestionSet ─────────────────────────

def activate_question_set(db: Session, question_set_id: int) -> Optional[QuestionSet]:
    qs = get_question_set(db, question_set_id)
    if not qs:
        return None

    # Deactivate all other active sets for same assessment
    db.query(QuestionSet).filter(
        QuestionSet.assessment_id == qs.assessment_id,
        QuestionSet.is_active == True,
        QuestionSet.id != qs.id
    ).update({QuestionSet.is_active: False})  # type: ignore

    qs.is_active = True  # type: ignore
    db.commit()
    db.refresh(qs)
    return qs
