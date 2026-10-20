import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

def test_connection():
    with driver.session(database=DATABASE) as session:
        result = session.run("RETURN 'Neo4j Connected!' AS message")
        print(result.single()["message"])