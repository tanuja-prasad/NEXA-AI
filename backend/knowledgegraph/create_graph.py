import json
from knowledgegraph.k_db import driver


def store_graph(data):

    # Convert JSON string to Python dictionary
    if isinstance(data, str):
        data = json.loads(data)

    with driver.session(database="knowledgegraph") as session:

        # Create entities
        for entity in data["entities"]:

            session.run(
                """
                MERGE (n:Entity {name: $name})
                SET n.type = $type
                """,
                name=entity["name"],
                type=entity["type"]
            )

        # Create relationships
        for relation in data["relationships"]:

            session.run(
                """
                MATCH (source:Entity {name: $source})
                MATCH (target:Entity {name: $target})

                MERGE (source)-[r:RELATED_TO {type: $relationship}]->(target)
                """,
                source=relation["source"],
                target=relation["target"],
                relationship=relation["relationship"]
            )

    print("Knowledge graph stored successfully")