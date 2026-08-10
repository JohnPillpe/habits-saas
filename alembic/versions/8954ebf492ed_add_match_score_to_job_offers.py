"""add match_score to job_offers

Revision ID: 8954ebf492ed
Revises: e061e146ceb5
Create Date: 2026-08-05 10:00:35.926616

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8954ebf492ed"
down_revision: Union[str, Sequence[str], None] = "e061e146ceb5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "job_offers",
        sa.Column("match_score", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("job_offers", "match_score")