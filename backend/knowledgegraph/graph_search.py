from knowledgegraph.k_db import driver


def graph_search(entities):

    results = []

    with driver.session(database="knowledgegraph") as session:

        for entity in entities:

            result = session.run("""
                MATCH (source:Entity)-[r]->(target:Entity)
                WHERE toLower(source.name) CONTAINS toLower($entity)
                   OR toLower(target.name) CONTAINS toLower($entity)

                RETURN
                    source.name AS source,
                    r.type AS relationship,
                    target.name AS target
            """, entity=entity)

            for record in result:

                results.append(
                    f"{record['source']} "
                    f"{record['relationship']} "
                    f"{record['target']}"
                )

    return results