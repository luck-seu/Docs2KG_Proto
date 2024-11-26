import argparse
import os
from pathlib import Path

import Docs2KG
from Docs2KG.parser.pdf.pdf2metadata import get_metadata_for_files, get_scanned_or_exported, PDF_TYPE_SCANNED
from Docs2KG.parser.pdf.pdf2blocks import PDF2Blocks
from Docs2KG.parser.pdf.pdf2tables import PDF2Tables
from Docs2KG.parser.pdf.pdf2text import PDF2Text
from Docs2KG.utils.get_logger import get_logger
from Docs2KG.utils.constants import DATA_INPUT_DIR
from dotenv import load_dotenv

logger = get_logger(__name__)
load_dotenv()


if __name__ == "__main__":
    """
    Loop a folder of pdf files and process them
    """

    pdf_file = DATA_INPUT_DIR / "2410.17600v1.pdf"
    
    scanned_or_exported = get_scanned_or_exported(pdf_file)
    if scanned_or_exported == PDF_TYPE_SCANNED:
        logger.info("This is a scanned pdf, we will handle it in another demo")
    else:
        pdf_2_blocks = PDF2Blocks(pdf_file)
        blocks_dict = pdf_2_blocks.extract_df(output_csv=True)
        logger.info(blocks_dict)

        pdf2tables = PDF2Tables(pdf_file)
        pdf2tables.extract2tables(output_csv=True)

        pdf_to_text = PDF2Text(pdf_file)
        text = pdf_to_text.extract2text(output_csv=True)
        md_text = pdf_to_text.extract2markdown(output_csv=True)
