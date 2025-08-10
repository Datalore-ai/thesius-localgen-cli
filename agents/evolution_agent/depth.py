base_instruction = """I want you to act as a Dataset Row Evolver.
You will receive a single JSON row (not the whole dataset), and your task is to modify this row in meaningful ways while keeping its schema exactly the same.
You must NOT remove or rename any keys in the JSON structure.
The number of rows is always 1 — treat this as a single data entry.
Make sure the output stays valid JSON.

The transformation strategy is:
{}

You may only modify field *values*, not keys. Keep changes small — around 10 to 20 words total.
Avoid saying '#Input Dataset#', '#Modified Dataset#', 'original row', or 'evolved row' in your output."""

def createConstraintsPrompt(row_json_str):
    prompt = base_instruction.format("Add constraints, clarifiers, or qualifiers to some of the field values — for example, change 'category': 'food' to 'category': 'food (perishable)' or 'priority': 'high' to 'priority': 'high and time-sensitive'.")
    prompt += "\n\n#Input Dataset#:\n{}\n".format(row_json_str)
    prompt += "#Modified Dataset#:\n"
    return prompt

def createDeepenPrompt(row_json_str):
    prompt = base_instruction.format("Make the content of some fields deeper or more layered — for example, change 'instruction': 'Write an essay about trees' to 'Write an essay about how deforestation impacts climate using real-world case studies'.")
    prompt += "\n\n#Input Dataset#:\n{}\n".format(row_json_str)
    prompt += "#Modified Dataset#:\n"
    return prompt

def createConcretizingPrompt(row_json_str):
    prompt = base_instruction.format("Replace vague or generic values with more specific ones. For instance, change 'topic': 'science' to 'topic': 'quantum physics' or 'audience': 'students' to 'audience': 'final-year computer science students'.")
    prompt += "\n\n#Input Dataset#:\n{}\n".format(row_json_str)
    prompt += "#Modified Dataset#:\n"
    return prompt

def createReasoningPrompt(row_json_str):
    prompt = base_instruction.format("Wherever applicable, increase the need for multi-step reasoning in the field values. For example, turn a simple 'question' into a multi-part one that requires combining facts or drawing inferences.")
    prompt += "\n\n#Input Dataset#:\n{}\n".format(row_json_str)
    prompt += "#Modified Dataset#:\n"
    return prompt
