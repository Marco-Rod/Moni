import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, IdMixin, TimestampMixin

# Debe coincidir con EMBEDDING_DIM (bge-m3 = 1024). Cambiarlo requiere migración y re-embedding.
EMBEDDING_DIM = 1024


class KnowledgeDocument(Base, IdMixin, TimestampMixin):
    """Documento de conocimiento. user_id NULL = conocimiento global (glosario, guías)."""

    __tablename__ = "knowledge_documents"

    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    source: Mapped[str | None] = mapped_column(String(500))


class KnowledgeChunk(Base, IdMixin, TimestampMixin):
    __tablename__ = "knowledge_chunks"
    __table_args__ = (UniqueConstraint("document_id", "chunk_index"),)

    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("knowledge_documents.id", ondelete="CASCADE"), index=True
    )
    chunk_index: Mapped[int]
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(Vector(EMBEDDING_DIM))
