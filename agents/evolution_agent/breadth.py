base_instruction = """I want you to act as a Dataset Row Creator.
You will receive a single JSON row (not a full dataset), and your goal is to create a brand-new data row that belongs to the **same domain** as the input.
The new row must:
- Follow the **same JSON schema** (same keys, structure).
- Be of **similar complexity and length**.
- Introduce a **different but related content** (not a simple rewording).
- Be fully understandable and valid as a training data row.

Do NOT use terms like '#Input Row#', '#New Row#', 'original row', or 'created row' in your response.
"""

def createBreadthPrompt(row_json_str):
    prompt = base_instruction
    prompt += "\n#Input Row#:\n{}\n".format(row_json_str)
    prompt += "#New Row#:\n"
    return prompt
