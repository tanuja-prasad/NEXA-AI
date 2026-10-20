from knowledgegraph.k_db import driver


def graph_search(query, limit=5):

    cypher = """
    MATCH (n)-[r]->(m)
    WHERE toLower(n.name) CONTAINS toLower($search_query)
       OR toLower(m.name) CONTAINS toLower($search_query)

    RETURN n.name AS source,
           type(r) AS relationship,
           m.name AS target

    LIMIT $result_limit
    """

    context = []

    with driver.session(database="knowledgegraph") as session:

        result = session.run(
            cypher,
            parameters={
                "search_query": query,
                "result_limit": limit
            }
        )

        for row in result:

            context.append(
                f"{row['source']} "
                f"{row['relationship']} "
                f"{row['target']}"
            )

    return context

if __name__ == "__main__":

    results = graph_search("data science")

    for result in results:
        print(result)