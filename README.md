# ChatWithSQLDB

## Overview

ChatWithSQLDB is a Streamlit application that enables users to interact with SQL databases using natural language queries. Leveraging the LangChain framework and OpenAI's language models, this tool translates user inputs into SQL commands, facilitating seamless database interactions without the need for manual SQL scripting.

## Features

- **Natural Language Processing**: Interpret and convert user queries into SQL statements.
- **Database Connectivity**: Supports connections to SQLite databases.
- **Interactive Interface**: Provides a user-friendly chat interface powered by Streamlit.

## Installation

To set up the ChatWithSQLDB application locally, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/akurapati1/ChatWithSQLDB.git
   cd ChatWithSQLDB
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv env
   ```

3. **Activate the Virtual Environment**:

   - On Windows:

     ```bash
     .\env\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source env/bin/activate
     ```

4. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` file includes all necessary packages, such as Streamlit and LangChain.

## Usage

1. **Prepare the Database**:

   Ensure you have an SQLite database (e.g., `student.db`) in the project directory. This database should contain the tables and data you intend to query.

2. **Run the Application**:

   ```bash
   streamlit run app.py
   ```

   This command will launch the Streamlit application, and a web browser window should open displaying the chat interface.

3. **Interact with the Database**:

   - In the chat interface, input your natural language queries related to the database content.
   - The application will process your input, convert it into an SQL query, execute it, and return the results in a readable format.

## Dependencies

The project relies on the following Python packages:

- `streamlit`
- `langchain`
- `sqlalchemy`
- `pysqlite3`

These dependencies are specified in the `requirements.txt` file and can be installed using the provided installation instructions.

