# NEXA – Memory-Augmented Knowledge Intelligence Assistant

NEXA is an AI-powered knowledge assistant that combines **Retrieval-Augmented Generation (RAG)**, **Knowledge Graphs**, **long-term memory**, and **web search** to provide intelligent and context-aware responses.

The system can understand a user's query and route it to the appropriate source such as the organization's knowledge base, knowledge graph, web search, or a general AI response.

---

## 🚀 Features

### 1. AI Chat Assistant
NEXA provides a conversational interface where users can ask questions in natural language.

### 2. Retrieval-Augmented Generation (RAG)

The system retrieves relevant information from the knowledge base before generating an answer.

The RAG pipeline helps the assistant provide answers based on the available organizational knowledge instead of relying only on the language model.

### 3. Knowledge Graph

NEXA uses a Neo4j Knowledge Graph to represent relationships between entities and retrieve connected information.

This helps improve retrieval for questions that require relationships between different entities.

### 4. Hybrid Retrieval

The system combines multiple retrieval approaches:

- Vector/semantic retrieval
- Knowledge Graph retrieval
- Hybrid retrieval

This allows NEXA to retrieve more relevant information for user queries.

### 5. Web Search

Queries that require current or external information can be routed to web search.

For example:

```text
What is today's weather in Pune?