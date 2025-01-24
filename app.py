import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
from sqlalchemy.exc import SQLAlchemyError
import mysql.connector

# Streamlit App Config
st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL DB")

# Constants
LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

# Sidebar: Select Database Option
radio_opt = ["Use SQLite 3 Database - Student.db", "Connect to MySQL Database"]
selected_opt = st.sidebar.radio(label="Choose the DB which you want to chat", options=radio_opt)

# Collect DB Credentials
if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("Provide MySQL Host", value="localhost")
    mysql_user = st.sidebar.text_input("MySQL User", value="root")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database")
else:
    db_uri = LOCALDB

# API Key for Groq LLM
api_key = st.sidebar.text_input(label="Groq API Key", type="password")

# Validations
if not api_key:
    st.error("🚨 Please add the Groq API Key.")
    st.stop()

if db_uri == MYSQL and not all([mysql_host, mysql_user, mysql_password, mysql_db]):
    st.error("🚨 Please provide all MySQL connection details.")
    st.stop()

# Initialize LLM Model with Exception Handling
try:
    llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)
except Exception as e:
    st.error(f"🚨 Failed to initialize LLM Model: {str(e)}")
    st.stop()


# Function to Configure Database
@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    try:
        if db_uri == LOCALDB:
            dbfilepath = (Path(__file__).parent / "student.db").absolute()
            creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
            return SQLDatabase(create_engine("sqlite:///", creator=creator))
        elif db_uri == MYSQL:
            return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
    except SQLAlchemyError as e:
        st.error(f"🚨 Database Connection Error: {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"🚨 Unexpected Error While Connecting to Database: {str(e)}")
        st.stop()


# Establish Database Connection
db = None
try:
    if db_uri == MYSQL:
        db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
    else:
        db = configure_db(db_uri)
except Exception as e:
    st.error(f"🚨 Database Initialization Error: {str(e)}")
    st.stop()

# Toolkit for LangChain SQL Agent
try:
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
except Exception as e:
    st.error(f"🚨 Failed to Initialize SQL Toolkit: {str(e)}")
    st.stop()

# SQL Agent Creation
try:
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )
except Exception as e:
    st.error(f"🚨 Error While Creating SQL Agent: {str(e)}")
    st.stop()

# Session State for Messages
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display Previous Messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User Input
user_query = st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        try:
            streamlit_callback = StreamlitCallbackHandler(st.container())
            response = agent.run(user_query, callbacks=[streamlit_callback])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
        except SQLAlchemyError as e:
            st.error(f"🚨 Database Query Error: {str(e)}")
        except Exception as e:
            st.error(f"🚨 Unexpected Error: {str(e)}")
