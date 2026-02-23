"""add school_classes table

Revision ID: e606d9847585
Revises: f85fd4bb2417
Create Date: 2026-02-23 12:xx:xx
"""

from alembic import op
import sqlalchemy as sa

# --- Alembic identifiers ---
revision = "e606d9847585"
down_revision = "f85fd4bb2417"
branch_labels = None
depends_on = None

def upgrade():
    # 1) Neue Tabelle
    op.create_table(
        "school_classes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=50), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 2) users: Spalte hinzufügen
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("school_class_id", sa.Integer(), nullable=True))

        # 3) FK Constraint mit Namen anlegen (WICHTIG!)
        batch_op.create_foreign_key(
            "fk_users_school_class_id",  # <-- Name des Constraints
            "school_classes",
            ["school_class_id"],
            ["id"],
        )

def downgrade():
    # FK entfernen, dann Spalte entfernen
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint("fk_users_school_class_id", type_="foreignkey")
        batch_op.drop_column("school_class_id")

    op.drop_table("school_classes")
