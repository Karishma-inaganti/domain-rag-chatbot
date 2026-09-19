from pathlib import Path
from pypdf import PdfReader


def load_pdfs(folder_path="documents"):
    documents = []

    folder = Path(folder_path)

    for pdf_file in folder.glob("*.pdf"):
        reader = PdfReader(pdf_file)

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()

            if text and text.strip():
                documents.append(
                    {
                        "text": text.strip(),
                        "metadata": {
                            "source": pdf_file.name,
                            "page": page_number,
                        },
                    }
                )

    return documents