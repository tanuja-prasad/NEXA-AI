from pydantic import BaseModel, Field
from typing import List
from rag.generator import load_llm


class Entity(BaseModel):
    name: str = Field(description="Name of the entity")
    type: str = Field(description="Type or category of the entity")


class Relationship(BaseModel):
    source: str = Field(description="Source entity")
    relationship: str = Field(description="Relationship between the entities")
    target: str = Field(description="Target entity")


class KnowledgeGraph(BaseModel):
    entities: List[Entity]
    relationships: List[Relationship]


llm = load_llm()

structured_llm = llm.with_structured_output(KnowledgeGraph)


def extract_relationships(text):

    prompt = f"""
You are a knowledge graph extraction system.

Analyze the following text.

Extract:
1. Important entities
2. Meaningful relationships between those entities

Only extract information that is explicitly supported by the text.
Do not invent entities or relationships.

Text:
{text}
"""

    result = structured_llm.invoke(prompt)

    return result.model_dump()