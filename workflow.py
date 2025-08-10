import json
import base64
import io
import fitz
import os
from pptx import Presentation
from PIL import Image
from docx import Document
from mistralai import Mistral
import asyncio

from qdrant_setup import *
from agents.generation_agent import generation_agent
from agents.schema_agent import generate_dataset_schema
from agents.evolution_agent.evolver import evolve_dataset
from utils import process_datagen_prompt


def encode_image_bytes(image_bytes: bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

def convert_to_pdf(file_bytes: bytes, filename: str):
    extension = filename.lower().split('.')[-1]

    if extension == "pdf":
        return file_bytes

    buffer = io.BytesIO()
    pdf = fitz.open()

    if extension in {"jpg", "jpeg", "png", "gif", "webp", "bmp"}:
        img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        img.save(buffer, format="PDF")
        return buffer.getvalue()

    elif extension in {"txt", "md"}:
        text = file_bytes.decode("utf-8", errors="ignore")
        page = pdf.new_page()
        page.insert_text((72, 72), text)
        pdf.save(buffer)
        return buffer.getvalue()

    elif extension in {"doc", "docx"}:
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join([para.text for para in doc.paragraphs])
        page = pdf.new_page()
        page.insert_text((72, 72), text)
        pdf.save(buffer)
        return buffer.getvalue()

    elif extension == "pptx":
        prs = Presentation(io.BytesIO(file_bytes))
        for slide in prs.slides:
            text = ""
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
            page = pdf.new_page()
            page.insert_text((72, 72), text)
        pdf.save(buffer)
        return buffer.getvalue()

    else:
        raise ValueError(f"Unsupported file type: {extension}")

def extract_pages_from_pdf_bytes(pdf_bytes: bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
    pages_data = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img_bytes = pix.tobytes("png")
        base64_image = encode_image_bytes(img_bytes)

        try:
            response = client.ocr.process(
                model="mistral-ocr-latest",
                document={"type": "image_url", "image_url": f"data:image/png;base64,{base64_image}"}
            )

            page_text = " ".join([p.markdown for p in response.pages]) if hasattr(response, 'pages') else ""
            pages_data.append({
                "page_number": page_num + 1,
                "content": page_text,
                "metadata": {
                    "dimensions": (pix.width, pix.height),
                    "rotation": page.rotation
                }
            })
            print(f"Processed page {page_num + 1}/{len(doc)}")

        except Exception as e:
            print(f"Error processing page {page_num + 1}: {str(e)}")
            pages_data.append({
                "page_number": page_num + 1,
                "content": "",
                "error": str(e)
            })

    return pages_data

def process_page(page_data: str, system_prompt: str):
    try:
        datarecords = generation_agent(page_data, system_prompt=system_prompt)
        return datarecords
    except Exception as e:
        print(f"QA generation failed for a page: {str(e)}")
    return []

async def generate_full_dataset(file_bytes: bytes, filename: str, system_prompt: str):
    yield f"📄 Converting '{filename}' to PDF...\n\n"
    converted_pdf_bytes = convert_to_pdf(file_bytes, filename)
    await asyncio.sleep(0.3)

    yield f"📑 Extracting pages from PDF...\n\n"
    pages = extract_pages_from_pdf_bytes(converted_pdf_bytes)
    total_pages = len(pages)
    await asyncio.sleep(0.3)

    dataset = []

    # Create chunks
    Chunks = []
    for page in pages:
        Chunks.append(page["content"])
    
    yield f"⚙️ Setting things up...\n\n"
    rag_pipeline_setup(user_id="test_user", documents=Chunks)

    Temp_Chunks = Chunks.copy()
    while len(Temp_Chunks) != 0:
        print(f"🧠 Generating your dataset - {int((len(Chunks)-len(Temp_Chunks))/len(Chunks) * 100)} % done")
        idx, current_chunk = select_random_chunk(Temp_Chunks)
        results = retrieve_from_store(current_chunk, user_id="test_user")

        # Context prep
        context = "\n\n\n\n".join(f"Page: {int(r.id)+1}\nContent: {r.payload['document']}" for r in results)

        page_qas = process_page(context, system_prompt)
        dataset.extend(page_qas)
        page_qas = evolve_dataset(page_qas)
        dataset.extend(page_qas)

        similar_chunks = [result.payload['document'] for result in results]

        for chunk in similar_chunks: 
            if chunk in Temp_Chunks:
                Temp_Chunks.remove(chunk)
    
    remove_data_from_store(user_id="test_user")
        
    yield f"Dataset generation completed with {len(dataset)} rows!\n\n"
    yield f"data:__DONE__:{json.dumps({'rows': dataset})}\n\n"
