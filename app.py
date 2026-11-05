"""Chat with a SQL database in natural language (Streamlit + LangChain SQL agent + Groq)."""
import os
import sqlite3
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_sql_agent
from langchain.callbacks import StreamlitCallbackHandler
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
SQLITE_PATH = (Path(__file__).parent / "student.db").absolute()
LOCAL_OPTION = "Use SQLite 3 Database - student.db"
MYSQL_OPTION = "Connect to MySQL Database"

st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL DB")

choice = st.sidebar.radio("Choose the DB which you want to chat with", [LOCAL_OPTION, MYSQL_OPTION])
mysql = {}
if choice == MYSQL_OPTION:
    mysql = {
        "host": st.sidebar.text_input("MySQL host", value="localhost"),
        "user": st.sidebar.text_input("MySQL user", value="root"),
        "password": st.sidebar.text_input("MySQL password", type="password"),
        "database": st.sidebar.text_input("MySQL database"),
    }
api_key = st.sidebar.text_input("Groq API key", type="password", value=os.getenv("GROQ_API_KEY", ""))

if not api_key:
    st.error("Please add the Groq API key.")
    st.stop()
if choice == MYSQL_OPTION and not all(mysql.values()):
    st.error("Please provide all MySQL connection details.")
    st.stop()


@st.cache_resource(ttl="2h")
def configure_db(use_mysql: bool, host=None, user=None, password=None, database=None) -> SQLDatabase:
    if not use_mysql:
        if not SQLITE_PATH.exists():
            raise FileNotFoundError(f"{SQLITE_PATH.name} not found - run `python sqlite.py` first.")
        # Read-only connection so the agent can never modify the sample data.
        creator = lambda: sqlite3.connect(f"file:{SQLITE_PATH}?mode=ro", uri=True)  # noqa: E731
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    # URL.create safely escapes special characters in credentials.
    url = URL.create("mysql+mysqlconnector", username=user, password=password, host=host, database=database)
    return SQLDatabase(create_engine(url))


try:
    db = configure_db(choice == MYSQL_OPTION, **mysql)
    llm = ChatGroq(groq_api_key=api_key, model_name=GROQ_MODEL, streaming=True)
    agent = create_sql_agent(
        llm=llm,
        toolkit=SQLDatabaseToolkit(db=db, llm=llm),
        verbose=True,
        agent_type="zero-shot-react-description",
        handle_parsing_errors=True,
    )
except (SQLAlchemyError, FileNotFoundError) as exc:
    st.error(f"Database error: {exc}")
    st.stop()
except Exception as exc:
    st.error(f"Failed to initialise the agent: {exc}")
    st.stop()

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question := st.chat_input("Ask anything about the database"):
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)
    with st.chat_message("assistant"):
        try:
            response = agent.invoke({"input": question}, {"callbacks": [StreamlitCallbackHandler(st.container())]})["output"]
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
        except SQLAlchemyError as exc:
            st.error(f"Database query error: {exc}")
        except Exception as exc:
            st.error(f"Unexpected error: {exc}")
