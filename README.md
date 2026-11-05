# ChatWithSQLDB

Ask questions about a SQL database in plain English. A **LangChain SQL agent** powered by a **Groq**-hosted LLM inspects the schema, writes the SQL, runs it and explains the result — all in a **Streamlit** chat UI.

## Features
- Natural-language → SQL → answer, with the agent's reasoning streamed live
- Works with the bundled **SQLite** sample (`student.db`, opened **read-only**) or any **MySQL** server
- Safe credential handling (`sqlalchemy.URL.create`), cached connections, graceful error messages
- Chat history with a one-click reset

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # add GROQ_API_KEY (or paste it in the sidebar)
python sqlite.py              # (re)creates student.db with sample data
streamlit run app.py
```

## Try these questions
- "How many students are in each class?"
- "Who has the highest marks?"
- "List students in DEVOPS scoring below 40."

## Sample schema
`STUDENT(NAME, CLASS, SECTION, MARKS)` — 5 seeded rows.

## Configuration
| Variable | Default |
|---|---|
| `GROQ_API_KEY` | – |
| `GROQ_MODEL` | `llama-3.1-8b-instant` |

## Notes
The SQLite connection is read-only. When pointing at MySQL, use a database user with **read-only** privileges — LLM-generated SQL should never run with write access.
