import json
from typing import List

from schemas import SchemaField
from configuration import CONFIGURATION

def process_datagen_prompt(fields: List[SchemaField]) -> str:
    schema_instruction = {field.key: field.description for field in fields}

    field_string = f"""## Response Format
Always respond with a valid JSON array of objects:
[
{json.dumps(schema_instruction, indent=2)},
// Additional entries...
]
"""
    return f"""
You are an expert Question-Answer generation assistant who has the skills of a polymath. Your task is to analyze content provided by the user and generate a comprehensive set of questions with detailed answers based on that content.

## Core Instructions

1. When presented with content, carefully analyze it to identify key concepts, important details, practical applications, and potential challenges or edge cases.

2. Generate a diverse set of questions and answers that thoroughly cover the provided content. Your response must be in valid JSON format.

3. Format code properly within JSON strings, using appropriate escape characters for special characters.

4. Number of dataset rows must be {CONFIGURATION["rows_per_context"]}

{field_string}
"""

