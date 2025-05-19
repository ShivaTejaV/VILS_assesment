# app/models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    Table,
    UniqueConstraint,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship, validates
from app.database import Base, SessionLocal

# Association table for QuestionSet ↔ Question (M2M)
question_set_questions = Table(
    "question_set_questions",
    Base.metadata,
    Column("question_set_id", Integer, ForeignKey("question_sets.id"), primary_key=True),
    Column("question_id",      Integer, ForeignKey("questions.id"),      primary_key=True),
)
class UserGroup(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)



    # Each group must have exactly one AssessmentType
    assessment_type_id = Column(Integer, ForeignKey("assessment_types.id"), nullable=False)
    assessment_type = relationship("AssessmentType")

    # One group can have many users
    users = relationship("User", back_populates="group")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    full_name = Column(String(150), nullable=True)
    hashed_password = Column(String(255), nullable=False)


    # Foreign key to the group this user belongs to
    group_id = Column(Integer, ForeignKey("user_groups.id"), nullable=False)
    group = relationship("UserGroup", back_populates="users")

    group_id = Column(Integer, ForeignKey("user_groups.id"), nullable=False)
    group = relationship("UserGroup", back_populates="users")

    # One user can have one submission per question set
    submissions = relationship("Submission", back_populates="user", cascade="all, delete-orphan")


class AssessmentType(Base):
    __tablename__ = "assessment_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    # One AssessmentType can have many Assessments
    assessments = relationship("Assessment", back_populates="type")


class Assessment(Base):
    __tablename__ = "assessments"
    __table_args__ = (
        UniqueConstraint("type_id", "version", name="uq_assessment_type_version"),
    )

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)

    type_id     = Column(Integer, ForeignKey("assessment_types.id", ondelete="RESTRICT"), nullable=False)
    type        = relationship("AssessmentType", back_populates="assessments")

    is_active   = Column(Boolean, default=False, nullable=False)
    version     = Column(Integer, default=1, nullable=False)

    question_sets = relationship("QuestionSet", back_populates="assessment")

    @validates("is_active")
    def _validate_single_active(self, key, value):
        if value:
            session = SessionLocal()
            existing = (
                session.query(Assessment)
                       .filter_by(type_id=self.type_id, is_active=True)
                       .first()
            )
            session.close()
            if existing and existing is not self:
                raise ValueError("There is already an active Assessment for this AssessmentType")
        return value

class QuestionSet(Base):
    __tablename__ = "question_sets"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(Integer, nullable=False, index=True)
    is_active = Column(Boolean, default=False, nullable=False)

    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    assessment = relationship("Assessment", back_populates="question_sets")

    # Many-to-many to Question
    questions = relationship(
        "Question",
        secondary=question_set_questions,
        back_populates="question_sets",
    )

    # Submissions against this set
    submissions = relationship("Submission", back_populates="question_set", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(1000), nullable=False)
    max_score = Column(Integer, nullable=False)

    # Many-to-many back to QuestionSet
    question_sets = relationship(
        "QuestionSet",
        secondary=question_set_questions,
        back_populates="questions",
    )

    # Versioned OptionSets
    option_sets = relationship("OptionSet", back_populates="question")


class OptionSet(Base):
    __tablename__ = "option_sets"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, nullable=True, index=True)
    version = Column(Integer, nullable=False, index=True)
    is_active = Column(Boolean, default=False, nullable=False)

    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    question = relationship("Question", back_populates="option_sets")

    options = relationship("Option", back_populates="option_set")

    @validates("is_active")
    def _validate_single_active(self, key, value):
        if value:
            session = SessionLocal()
            existing = (
                session.query(OptionSet)
                .filter_by(question_id=self.question_id, is_active=True)
                .first()
            )
            session.close()
            if existing and existing is not self:
                raise ValueError(
                    "There is already an active OptionSet for this Question"
                )
        return value


class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(500), nullable=False)
    score = Column(Integer, nullable=False)

    option_set_id = Column(Integer, ForeignKey("option_sets.id"), nullable=False)
    option_set = relationship("OptionSet", back_populates="options")

    @validates("score")
    def validate_score(self, key, value):
        session = SessionLocal()
        question = session.get(Question, self.option_set.question_id)
        session.close()
        if question is None:
            raise ValueError("Parent Question not found for this OptionSet")
        if value > question.max_score:
            raise ValueError(
                f"Option score {value} exceeds question’s max_score {question.max_score}"
            )
        return value


class Submission(Base):
    __tablename__ = "submissions"
    __table_args__ = (
        UniqueConstraint("user_id", "question_set_id", name="uq_submission_per_user_per_qset"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_set_id = Column(Integer, ForeignKey("question_sets.id"), nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="submissions")
    question_set = relationship("QuestionSet", back_populates="submissions")
    responses = relationship("Response", back_populates="submission", cascade="all, delete-orphan")


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    option_id = Column(Integer, ForeignKey("options.id"), nullable=False)

    submission = relationship("Submission", back_populates="responses")
    question = relationship("Question")
    option = relationship("Option")

