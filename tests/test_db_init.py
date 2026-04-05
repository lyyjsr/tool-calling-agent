from sqlalchemy import inspect

from app.db.database import engine
from app.db.init_db import init_db


def test_init_db_creates_required_tables() -> None:
    init_db()

    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())

    assert "sessions" in table_names
    assert "messages" in table_names
    assert "tasks" in table_names
    assert "review_tasks" in table_names