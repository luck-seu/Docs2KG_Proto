from Docs2KG.kg.pdf_layout_kg import PDFLayoutKG
from Docs2KG.kg.semantic_kg import SemanticKG
from Docs2KG.kg.utils.json2triplets import JSON2Triplets
from Docs2KG.kg.utils.neo4j_connector import Neo4jLoader
from Docs2KG.modules.llm.markdown2json import LLMMarkdown2Json
from Docs2KG.parser.pdf.pdf2blocks import PDF2Blocks
from Docs2KG.parser.pdf.pdf2metadata import PDF_TYPE_SCANNED, get_scanned_or_exported
from Docs2KG.parser.pdf.pdf2tables import PDF2Tables
from Docs2KG.parser.pdf.pdf2text import PDF2Text
from Docs2KG.utils.constants import DATA_INPUT_DIR, DATA_OUTPUT_DIR
from Docs2KG.utils.get_logger import get_logger
import os
from dotenv import load_dotenv
load_dotenv()
logger = get_logger(__name__)

if __name__ == "__main__":
    pdf_name = "2410.17600v1.pdf"
    output_folder = DATA_OUTPUT_DIR / pdf_name
    input_md_file = output_folder / "texts" / "md.csv"

    markdown2json = LLMMarkdown2Json(
        input_md_file,
        llm_model_name="qwen2.5-coder:32b",
    )
    markdown2json.extract2json()

    # after this we will have a added `md.json.csv` in the `texts` folder

    # next we will start to extract the layout knowledge graph first

    layout_kg = PDFLayoutKG(output_folder)
    layout_kg.create_kg()
    # After this, you will have the layout.json in the `kg` folder

    # then we add the semantic knowledge graph
    semantic_kg = SemanticKG(output_folder, llm_enabled=True)
    semantic_kg.add_semantic_kg()

    # After this, the layout_kg.json will be augmented with the semantic connections
    # in the `kg` folder

    # then we do the triplets extraction
    json_2_triplets = JSON2Triplets(output_folder)
    json_2_triplets.transform()

    # After this, you will have the triplets_kg.json in the `kg` folder
    # You can take it from here, load it into your graph db, or handle it in any way you want

    # If you want to load it into Neo4j, you can refer to the `examples/kg/utils/neo4j_connector.py`
    # to get it quickly loaded into Neo4j
    # You can do is run the `docker compose -f examples/compose/docker-compose.yml up`
    # So we will have a Neo4j instance running, then you can run the `neo4j_connector.py` to load the data
    uri = os.environ["NEO4J_URI"]  # if it is a remote graph db, you can change it to the remote uri
    username = os.environ["NEO4J_USERNAME"]
    password = os.environ["NEO4J_PASSWORD"]
    json_file_path = output_folder / "kg" / "triplets_kg.json"

    neo4j_loader = Neo4jLoader(uri, username, password, json_file_path, clean=True)
    neo4j_loader.load_data()
    neo4j_loader.close()