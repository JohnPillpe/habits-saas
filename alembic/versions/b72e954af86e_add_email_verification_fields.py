"""add email verification fields

Revision ID: b72e954af86e
Revises: 8954ebf492ed
Create Date: 2026-08-17
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b72e954af86e"
down_revision: Union[str, Sequence[str], None] = "8954ebf492ed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add as nullable first so existing users are not broken
    op.add_column(
        "usuarios",
        sa.Column(
            "email_verified",
            sa.Boolean(),
            nullable=True,
        ),
    )

    # 2. Existing users are considered verified
    op.execute(
        "UPDATE usuarios SET email_verified = TRUE "
        "WHERE email_verified IS NULL"
    )

    # 3. From now on the field cannot be NULL
    op.alter_column(
        "usuarios",
        "email_verified",
        existing_type=sa.Boolean(),
        nullable=False,
        server_default=sa.text("false"),
    )

    # 4. Verification token fields
    op.add_column(
        "usuarios",
        sa.Column(
            "email_verification_token",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.create_unique_constraint(
        "uq_usuarios_email_verification_token",
        "usuarios",
        ["email_verification_token"],
    )

    op.add_column(
        "usuarios",
        sa.Column(
            "email_verification_expires",
            sa.DateTime(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "usuarios",
        "email_verification_expires",
    )

    op.drop_constraint(
        "uq_usuarios_email_verification_token",
        "usuarios",
        type_="unique",
    )

    op.drop_column(
        "usuarios",
        "email_verification_token",
    )

    op.drop_column(
        "usuarios",
        "email_verified",
    )