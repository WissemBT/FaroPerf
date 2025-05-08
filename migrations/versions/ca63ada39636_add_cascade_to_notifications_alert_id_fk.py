"""Add cascade to notifications.alert_id FK

Revision ID: ca63ada39636
Revises: fd42a6edc5fa
Create Date: 2025-05-08 18:14:07.235338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca63ada39636'
down_revision: Union[str, None] = 'fd42a6edc5fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# --------------------------------------------------------------------------- #
# Helper section – list every FK that must be recreated with ON DELETE CASCADE
# --------------------------------------------------------------------------- #
# ⬇  (table_name, fk_name, local_col, referred_table, referred_col)
FKS = [
    ("alerts",         "alerts_server_id_fkey",     "server_id",     "servers",      "server_id"),
    ("alerts",         "alerts_rule_id_fkey",       "rule_id",       "alert_rules",  "rule_id"),
    ("alert_rules",    "alert_rules_server_id_fkey","server_id",     "servers",      "server_id"),
    ("metrics",        "metrics_server_id_fkey",    "server_id",     "servers",      "server_id"),
    ("api_keys",       "api_keys_server_fkey",      "server",        "servers",      "server_id"),
    ("servers",        "servers_user_id_fkey",      "user_id",       "users",        "user_id"),
    ("notifications",  "notifications_user_id_fkey","user_id",       "users",        "user_id"),
    ("notifications",  "notifications_alert_id_fkey","alert_id",     "alerts",       "alert_id"),
]


# ------------------------ #
# Upgrade / Downgrade code #
# ------------------------ #
def upgrade() -> None:
    """
    Drop each old FK → recreate identical FK with ON DELETE CASCADE
    """
    for tbl, fk_name, col, ref_tbl, ref_col in FKS:
        op.drop_constraint(fk_name, tbl, type_="foreignkey")
        op.create_foreign_key(
            fk_name,
            source_table=tbl,
            referent_table=ref_tbl,
            local_cols=[col],
            remote_cols=[ref_col],
            ondelete="CASCADE",
        )


def downgrade() -> None:
    """
    Reverse: drop CASCADE version → recreate WITHOUT CASCADE
    """
    for tbl, fk_name, col, ref_tbl, ref_col in FKS:
        op.drop_constraint(fk_name, tbl, type_="foreignkey")
        op.create_foreign_key(
            fk_name,
            source_table=tbl,
            referent_table=ref_tbl,
            local_cols=[col],
            remote_cols=[ref_col],
            # no ondelete ⇒ default RESTRICT behaviour
        )