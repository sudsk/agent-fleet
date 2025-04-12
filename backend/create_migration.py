#!/usr/bin/env python3
"""
Script to create an initial migration for the AgentFleet database.
"""
import os
import subprocess
import sys

def create_initial_migration():
    """Creates an initial migration for the database."""
    try:
        print("Creating initial migration...")
        
        # Make sure the migrations directory exists
        os.makedirs('migrations/versions', exist_ok=True)
        
        # Run alembic to create the migration
        subprocess.run(
            ['alembic', 'revision', '--autogenerate', '-m', 'Initial migration'],
            check=True
        )
        
        print("Migration created successfully!")
        print("To apply the migration, run: alembic upgrade head")
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating migration: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    create_initial_migration()
