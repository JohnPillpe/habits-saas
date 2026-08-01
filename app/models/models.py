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


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    habitos: Mapped[list["Habit"]] = relationship(
        "Habit",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

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


# MODIFICA LA CLASE Habit EXISTENTE para añadir usuario_id:
class Habit(Base):
    __tablename__ = "habitos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(500), nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # NUEVA COLUMNA (AÑADE ESTA LÍNEA):
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)

    registros: Mapped[list["Registro"]] = relationship("Registro", back_populates="habito", cascade="all, delete-orphan")
    
    # NUEVA RELACIÓN (AÑADE ESTA LÍNEA):
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="habitos")


class Registro(Base):
    __tablename__ = "registros"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)  
    habitos_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("habitos.id"), nullable=False
    )
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    completado: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    habito: Mapped["Habit"] = relationship("Habit", back_populates="registros")


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

    enlace: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    usuario_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
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