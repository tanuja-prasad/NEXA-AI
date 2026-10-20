import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

if not all([uri, username, password]):
    print("Missing Neo4j environment variables.")
else:
    try:
        with GraphDatabase.driver(
            uri,
            auth=(username, password)
        ) as driver:
            driver.verify_connectivity()
            print("Neo4j connection successful!")

    except Exception as e:
        print(f"Neo4j connection failed: {type(e).__name__}: {e}")