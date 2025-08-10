import json
from dotenv import load_dotenv

from schemas import DatasetSchema
from agents.client_initialization import openai_client
from prompts import schema_generate_prompt

load_dotenv()

def generate_dataset_schema(
    user_concept: str, model: str = "gpt-4.1-mini"
) -> DatasetSchema:
    response = openai_client.responses.parse(
        model=model,
        input=[
            {"role": "system", "content": schema_generate_prompt},
            {"role": "user", "content": user_concept},
        ],
        text_format=DatasetSchema,
    )

    result = response.output_parsed
    return result