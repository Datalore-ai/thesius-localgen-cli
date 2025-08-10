import time
import json
from dotenv import load_dotenv
from pydantic import ValidationError
from openai import RateLimitError, OpenAIError
from agents.client_initialization import openai_client

from schemas import DatasetRecords

load_dotenv()

def generation_agent(content, system_prompt, model="gpt-4.1-mini", retries=3, base_wait=2):
    for attempt in range(retries):
        try:
            response = openai_client.responses.create(
                model=model,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content}
                ],
                temperature=0.2,
            )

            raw_text = response.output_text.strip()

            if raw_text.startswith("```json"):
                raw_text = raw_text[len("```json"):].lstrip()
            elif raw_text.startswith("```"):
                raw_text = raw_text[len("```"):].lstrip()

            if raw_text.endswith("```"):
                raw_text = raw_text[:-3].rstrip()

            parsed_json = json.loads(raw_text)
            final_package = {"dataset": parsed_json}
            validated = DatasetRecords(**final_package)

            return validated.dataset

        except json.JSONDecodeError as e:
            print(f"[JSON Parse Error] {e}")
            return []

        except ValidationError as e:
            print(f"[Pydantic Validation Error] {e}")
            return []

        except RateLimitError:
            wait_time = base_wait * (2 ** attempt)
            print(f"[Rate Limit] Retrying in {wait_time}s (Attempt {attempt + 1}/{retries})...")
            time.sleep(wait_time)

        except OpenAIError as e:
            print(f"[OpenAI Error] {e}")
            return []

    print("[Rate limit Error] Exceeded retry attempts due to rate limiting.")
    return []
