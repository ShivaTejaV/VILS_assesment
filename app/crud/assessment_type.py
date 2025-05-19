from sqlalchemy.orm import Session
from models import AssessmentType
from schemas import AssessmentTypeCreate, AssessmentTypeRead


def create_assessment_type(db: Session, assessment_type: AssessmentTypeCreate):
    db_assessment_type = AssessmentType(name=assessment_type.name)
    db.add(db_assessment_type)
    db.commit()
    db.refresh(db_assessment_type)
    return db_assessment_type


def get_assessment_type(db: Session, assessment_type_id: int):
    return db.query(AssessmentType).filter(AssessmentType.id == assessment_type_id).first()


def get_assessment_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AssessmentType).offset(skip).limit(limit).all()
