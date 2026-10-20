from preprocessing_chunks.chunk import get_chunks
from knowledgegraph.extractor import extract_relationships
from knowledgegraph.create_graph import store_graph


def build_knowledge_graph():

    chunks = get_chunks()

    print("Total chunks:", len(chunks))

    for i, chunk in enumerate(chunks):

        print(f"\nProcessing chunk {i + 1}/{len(chunks)}")

        try:

            # Extract entities and relationships
            graph_data = extract_relationships(chunk)

            print("Entities:", len(graph_data["entities"]))
            print("Relationships:", len(graph_data["relationships"]))

            # Store in Neo4j
            store_graph(graph_data)

            print("Stored successfully.")

        except Exception as e:

            print(f"Error in chunk {i + 1}: {e}")


if __name__ == "__main__":
    build_knowledge_graph()