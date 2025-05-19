from sqlalchemy.orm import Session
from models import Assessment
from schemas import AssessmentCreate
from typing import List, Optional

def create_assessment(db: Session, assessment: AssessmentCreate):
    # Get latest version for this type_id
    last_version = (
        db.query(Assessment)
          .filter(Assessment.type_id == assessment.type_id)
          .order_by(Assessment.version.desc())
          .first()
    )

    new_version = (last_version.version + 1) if last_version else 1

    db_assessment = Assessment(
        title=assessment.title,
        description=assessment.description,
        type_id=assessment.type_id,
        version=new_version,
        is_active=False  # Always inactive on creation
    )

    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment

# ─────────────────────────────────────────────────────────────
# Get single assessment by ID
# ─────────────────────────────────────────────────────────────

def get_assessment(db: Session, assessment_id: int) -> Optional[Assessment]:
    return db.query(Assessment).filter(Assessment.id == assessment_id).first()

# ─────────────────────────────────────────────────────────────
# Get list of assessments (pagination)
# ─────────────────────────────────────────────────────────────

def get_assessments(db: Session, skip: int = 0, limit: int = 100) -> List[Assessment]:
    return db.query(Assessment).offset(skip).limit(limit).all()

# ─────────────────────────────────────────────────────────────
# Activate assessment by ID (ensure only one active per type_id)
# ─────────────────────────────────────────────────────────────

def activate_assessment(db: Session, assessment_id: int) -> Optional[Assessment]:
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        return None

    # Deactivate existing active assessment for same type_id
    db.query(Assessment)\
      .filter(
          Assessment.type_id == assessment.type_id,
          Assessment.is_active == True,
          Assessment.id != assessment.id
      )\
      .update({Assessment.is_active: False})

    # Activate selected one
    assessment.is_active = True # type: ignore
    db.commit()
    db.refresh(assessment)
    return assessment


# ─────────────────────────────────────────────────────────────
# get active assessment by assessment type (ensure only one active per assesment type)
# ─────────────────────────────────────────────────────────────

def get_active_assessment_by_type(db: Session, type_id: int):
    return (
        db.query(Assessment)
        .filter(Assessment.type_id == type_id, Assessment.is_active == True)
        .first()
    )


