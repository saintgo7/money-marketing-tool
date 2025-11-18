#!/usr/bin/env python
"""Initialize the database with tables"""

from src.models.database import init_db

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("✓ Database tables created successfully!")
