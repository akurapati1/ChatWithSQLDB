"""Create (or reset) the sample SQLite database `student.db` used by the app."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "student.db"

SAMPLE_ROWS = [
    ("Krish", "Data Science", "A", 90),
    ("John", "Data Science", "B", 100),
    ("Mukesh", "Data Science", "A", 86),
    ("Jacob", "DEVOPS", "A", 50),
    ("Dipesh", "DEVOPS", "A", 35),
]


def seed(path: Path = DB_PATH) -> None:
    with sqlite3.connect(path) as conn:
        conn.execute("DROP TABLE IF EXISTS STUDENT")
        conn.execute("CREATE TABLE STUDENT (NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT)")
        conn.executemany("INSERT INTO STUDENT VALUES (?, ?, ?, ?)", SAMPLE_ROWS)
        print("Inserted records:")
        for row in conn.execute("SELECT * FROM STUDENT"):
            print(row)


if __name__ == "__main__":
    seed()
