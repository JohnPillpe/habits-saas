from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

from sqlalchemy import Column



class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    ofertas: Mapped[list["JobOffer"]] = relationship(
        "JobOffer",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    documentos: Mapped[list["Document"]] = relationship(
        "Document",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )


class JobOffer(Base):
    __tablename__ = "job_offers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    titulo: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    descripcion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    empresa: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    categoria: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    salario: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    tags: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    pais: Mapped[str | None] = mapped_column(
    String(255),
    nullable=True,
    )

    ciudad: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    tipo_trabajo: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    publicado_en: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )





    country: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    work_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    source: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    logo: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )



    enlace: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    usuario_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    match_score: Mapped[int | None] = mapped_column(
    Integer,
    nullable=True,
    )

    usuario: Mapped["Usuario"] = relationship(
    "Usuario",
    back_populates="ofertas"
    )


class CareerAnalysis(Base):
    __tablename__ = "career_analysis"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    job_offer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("job_offers.id"),
        unique=True,
        nullable=False,
    )

    match_score: Mapped[int] = mapped_column(Integer)

    candidate_summary: Mapped[str] = mapped_column(Text)

    job_summary: Mapped[str] = mapped_column(Text)

    strengths: Mapped[list] = mapped_column(JSON)

    missing_skills: Mapped[list] = mapped_column(JSON)

    improvements: Mapped[list] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    job_offer: Mapped["JobOffer"] = relationship("JobOffer")

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    usuario_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    nombre: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    tipo: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    fecha_subida: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="documentos"
    )

class OptimizedCV(Base):
    __tablename__ = "optimized_cvs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    job_offer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("job_offers.id"),
        unique=True,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    job_offer: Mapped["JobOffer"] = relationship("JobOffer")


class CoverLetter(Base):
    __tablename__ = "cover_letters"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    job_offer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("job_offers.id"),
        unique=True,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    job_offer: Mapped["JobOffer"] = relationship("JobOffer")

class ApplicationAnswers(Base):
    __tablename__ = "application_answers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    job_offer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("job_offers.id"),
        unique=True,
        nullable=False,
    )

    tell_me_about_yourself: Mapped[str] = mapped_column(Text)

    why_this_company: Mapped[str] = mapped_column(Text)

    why_should_we_hire_you: Mapped[str] = mapped_column(Text)

    greatest_strength: Mapped[str] = mapped_column(Text)

    greatest_weakness: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    job_offer: Mapped["JobOffer"] = relationship("JobOffer")

class InterviewPreparation(Base):
    __tablename__ = "interview_preparation"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    job_offer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("job_offers.id"),
        unique=True,
        nullable=False,
    )

    technical_questions: Mapped[list] = mapped_column(JSON)

    behavioral_questions: Mapped[list] = mapped_column(JSON)

    tips: Mapped[list] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    job_offer: Mapped["JobOffer"] = relationship("JobOffer")

class UserJobPreference(Base):
    __tablename__ = "user_job_preferences"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("usuarios.id"),
        unique=True,
        nullable=False,
    )

    desired_role: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    target_countries: Mapped[list] = mapped_column(
        JSON,
        default=list,
    )

    target_cities: Mapped[list] = mapped_column(
        JSON,
        default=list,
    )

    remote: Mapped[bool] = mapped_column(Boolean, default=True)

    hybrid: Mapped[bool] = mapped_column(Boolean, default=False)

    onsite: Mapped[bool] = mapped_column(Boolean, default=False)

    published_within_days: Mapped[int] = mapped_column(
        Integer,
        default=7,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    usuario: Mapped["Usuario"] = relationship("Usuario")

class InterviewSession(Base):
    __tablename__ = "interview_sessions"



    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("usuarios.id"))

    role = Column(String)

    current_question = Column(Integer, default=0)

    score = Column(Integer, default=0)

    answers = Column(JSON, default=list)

    finished = Column(Boolean, default=False)

    usuario = relationship("Usuario")