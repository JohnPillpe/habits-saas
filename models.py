from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relación: un usuario tiene muchos hábitos
    habitos: Mapped[list["Habit"]] = relationship("Habit", back_populates="usuario", cascade="all, delete-orphan")
    ofertas: Mapped[list["JobOffer"]] = relationship("JobOffer", back_populates="usuario", cascade="all, delete-orphan")


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
