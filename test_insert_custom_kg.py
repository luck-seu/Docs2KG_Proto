import os
import json
from lightrag.utils import EmbeddingFunc
from lightrag import LightRAG, QueryParam
from lightrag.llm import ollama_model_complete, ollama_embedding
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
load_dotenv()


# Constants
WORKING_DIR = "./lightrag_working_dir/insert_custom_kg"
# logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

# Neo4j connection credentials
NEO4J_URI = os.environ["NEO4J_URI"]
NEO4J_USERNAME = os.environ["NEO4J_USERNAME"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]


def main():
    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=ollama_model_complete,
        llm_model_name="qwen2.5-coder:32b",
        llm_model_max_async=4,
        llm_model_max_token_size=32768,
        llm_model_kwargs={"host": "http://localhost:11434", "options": {"num_ctx": 32768}},
        embedding_func=EmbeddingFunc(
            embedding_dim=768,
            max_token_size=8192,
            func=lambda texts: ollama_embedding(
                texts, embed_model="nomic-embed-text:latest", host="http://localhost:11434"
            ),
        ),
    )
    
    custom_kg = {
        "entities": [
            {
                "entity_name": "CompanyA",
                "entity_type": "Organization",
                "description": "A major technology company",
                "source_id": "Source1"
            },
            {
                "entity_name": "ProductX",
                "entity_type": "Product",
                "description": "A popular product developed by CompanyA",
                "source_id": "Source1"
            }
        ],
        "relationships": [
            {
                "src_id": "CompanyA",
                "tgt_id": "ProductX",
                "description": "CompanyA develops ProductX",
                "keywords": "develop, produce",
                "weight": 1.0,
                "source_id": "Source1"
            }
        ]
    }
    rag.insert_custom_kg(custom_kg)
    query_result = rag.query("What is the relation between CompanyA and ProductX?", param=QueryParam(mode="local"))
    print(query_result)


if __name__ == "__main__":
    main()
