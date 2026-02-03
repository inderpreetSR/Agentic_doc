"""
Database utilities for storing custom diagrams and user preferences.
Uses SQLite for simplicity - can be upgraded to PostgreSQL for production.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

# Database file location
DB_DIR = Path(__file__).parent.parent / "data"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "dsaa_agents.db"


@contextmanager
def get_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_database():
    """Initialize database tables."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Custom diagrams table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS custom_diagrams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                diagram_type TEXT NOT NULL,
                mermaid_code TEXT NOT NULL,
                filters JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_public BOOLEAN DEFAULT 0,
                user_id TEXT
            )
        """)

        # User preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                preferences JSON NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Diagram templates table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diagram_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                mermaid_code TEXT NOT NULL,
                preview_filters JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Usage history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usage_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                action TEXT NOT NULL,
                details JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()


# Initialize database on module import
init_database()


class DiagramRepository:
    """Repository for custom diagram CRUD operations."""

    @staticmethod
    def create(
        name: str,
        mermaid_code: str,
        diagram_type: str = "flowchart",
        description: str = "",
        filters: Optional[dict] = None,
        is_public: bool = False,
        user_id: Optional[str] = None,
    ) -> int:
        """
        Create a new custom diagram.

        Returns:
            ID of the created diagram
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO custom_diagrams
                (name, description, diagram_type, mermaid_code, filters, is_public, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (name, description, diagram_type, mermaid_code,
                 json.dumps(filters) if filters else None, is_public, user_id)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_by_id(diagram_id: int) -> Optional[Dict[str, Any]]:
        """Get a diagram by ID."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM custom_diagrams WHERE id = ?",
                (diagram_id,)
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    @staticmethod
    def get_all(user_id: Optional[str] = None, include_public: bool = True) -> List[Dict[str, Any]]:
        """Get all diagrams, optionally filtered by user."""
        with get_connection() as conn:
            cursor = conn.cursor()

            if user_id:
                if include_public:
                    cursor.execute(
                        "SELECT * FROM custom_diagrams WHERE user_id = ? OR is_public = 1 ORDER BY updated_at DESC",
                        (user_id,)
                    )
                else:
                    cursor.execute(
                        "SELECT * FROM custom_diagrams WHERE user_id = ? ORDER BY updated_at DESC",
                        (user_id,)
                    )
            else:
                cursor.execute(
                    "SELECT * FROM custom_diagrams WHERE is_public = 1 ORDER BY updated_at DESC"
                )

            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def update(
        diagram_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        mermaid_code: Optional[str] = None,
        filters: Optional[dict] = None,
        is_public: Optional[bool] = None,
    ) -> bool:
        """Update a diagram."""
        updates = []
        values = []

        if name is not None:
            updates.append("name = ?")
            values.append(name)
        if description is not None:
            updates.append("description = ?")
            values.append(description)
        if mermaid_code is not None:
            updates.append("mermaid_code = ?")
            values.append(mermaid_code)
        if filters is not None:
            updates.append("filters = ?")
            values.append(json.dumps(filters))
        if is_public is not None:
            updates.append("is_public = ?")
            values.append(is_public)

        if not updates:
            return False

        updates.append("updated_at = CURRENT_TIMESTAMP")
        values.append(diagram_id)

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE custom_diagrams SET {', '.join(updates)} WHERE id = ?",
                values
            )
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(diagram_id: int) -> bool:
        """Delete a diagram."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM custom_diagrams WHERE id = ?",
                (diagram_id,)
            )
            conn.commit()
            return cursor.rowcount > 0


class PreferencesRepository:
    """Repository for user preferences."""

    @staticmethod
    def get(user_id: str) -> Dict[str, Any]:
        """Get user preferences."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT preferences FROM user_preferences WHERE user_id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            if row:
                return json.loads(row["preferences"])
            return {}

    @staticmethod
    def save(user_id: str, preferences: Dict[str, Any]) -> bool:
        """Save user preferences (upsert)."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO user_preferences (user_id, preferences)
                VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    preferences = excluded.preferences,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (user_id, json.dumps(preferences))
            )
            conn.commit()
            return True


class TemplateRepository:
    """Repository for diagram templates."""

    @staticmethod
    def get_all(category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all templates, optionally filtered by category."""
        with get_connection() as conn:
            cursor = conn.cursor()

            if category:
                cursor.execute(
                    "SELECT * FROM diagram_templates WHERE category = ? ORDER BY name",
                    (category,)
                )
            else:
                cursor.execute("SELECT * FROM diagram_templates ORDER BY category, name")

            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def create(
        name: str,
        category: str,
        mermaid_code: str,
        description: str = "",
        preview_filters: Optional[dict] = None,
    ) -> int:
        """Create a new template."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO diagram_templates (name, category, description, mermaid_code, preview_filters)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name, category, description, mermaid_code,
                 json.dumps(preview_filters) if preview_filters else None)
            )
            conn.commit()
            return cursor.lastrowid


class HistoryRepository:
    """Repository for usage history."""

    @staticmethod
    def log(action: str, details: Optional[dict] = None, user_id: Optional[str] = None):
        """Log a usage event."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO usage_history (user_id, action, details)
                VALUES (?, ?, ?)
                """,
                (user_id, action, json.dumps(details) if details else None)
            )
            conn.commit()

    @staticmethod
    def get_recent(limit: int = 100, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get recent history entries."""
        with get_connection() as conn:
            cursor = conn.cursor()

            if user_id:
                cursor.execute(
                    "SELECT * FROM usage_history WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
                    (user_id, limit)
                )
            else:
                cursor.execute(
                    "SELECT * FROM usage_history ORDER BY created_at DESC LIMIT ?",
                    (limit,)
                )

            return [dict(row) for row in cursor.fetchall()]
