import os
import asyncio
import asyncpg


async def run_migrations():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")

    conn = await asyncpg.connect(database_url)

    try:
        # create migrations table if it doesn't exist
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS migrations (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                applied_at TIMESTAMP NOT NULL DEFAULT (NOW())
            )
        """
        )

        # get applied migrations from db
        applied_migrations = await conn.fetch("SELECT filename FROM migrations")
        applied_filenames = {row["filename"] for row in applied_migrations}

        # get migration files from migrations dir
        migration_dir = "migrations"
        # files are named for sort to work, 001_, 002_, etc
        migration_files = sorted(
            [f for f in os.listdir(migration_dir) if f.endswith(".sql")]
        )

        # run unapplied migrations in order
        for filename in migration_files:
            if filename not in applied_filenames:
                print(f"Applying migration: {filename}")
                with open(os.path.join(migration_dir, filename), "r") as f:
                    sql = f.read()
                await conn.execute(sql)
                await conn.execute(
                    "INSERT INTO migrations (filename) VALUES ($1)", filename
                )
                print(f"Applied migration: {filename}")

        print("All migrations applied successfully")

    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(run_migrations())
