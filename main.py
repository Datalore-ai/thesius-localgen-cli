import json
import asyncio

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich import box
from pyfiglet import Figlet
from datetime import datetime

from workflow import generate_dataset_schema, generate_full_dataset, process_datagen_prompt

console = Console()

def render_banner(title: str = "Datalore.ai", subtitle: str = "Document to Dataset Generator"):
    figlet = Figlet(font="banner3-D", width=200)
    ascii_art = figlet.renderText(title)
    panel = Panel.fit(
        f"[bold cyan]{ascii_art}[/bold cyan]\n[green]{subtitle}[/green]",
        border_style="magenta",
        padding=(1, 4),
        title="[bold yellow]WELCOME[/bold yellow]",
        box=box.DOUBLE
    )
    console.print(panel)

def render_schema(schema_obj):
    if not hasattr(schema_obj, 'generated_schema'):
        print_section("SCHEMA GENERATION", str(schema_obj))
        return

    table = Table(title=None, box=box.ASCII, header_style="bold magenta")
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Type", style="green")
    table.add_column("Description", style="white")

    for field in schema_obj.generated_schema:
        field_type = str(field.type.value if hasattr(field.type, "value") else field.type)
        table.add_row(field.key, field_type, field.description)

    console.print("\n")
    print_section("SCHEMA GENERATION")
    console.print(table)

def print_section(title: str, content: str = "", width: int = 100):
    title_bar = f" {title} ".center(width, "=")
    console.print(f"\n[bold cyan]{title_bar}[/bold cyan]")
    if content:
        console.print(content)

def status(message: str, style="bold white"):
    console.print(f"[{style}]• {message}[/{style}]")

def success(message: str):
    console.print(f"[bold green]{message}[/bold green]")

def warning(message: str):
    console.print(f"[bold yellow]{message}[/bold yellow]")

def error(message: str):
    console.print(f"[bold red]{message}[/bold red]")

def get_user_feedback(fields, base_query):
    while True:
        render_schema(fields)
        status("Do you want to proceed with this schema?")
        feedback = input("Type your feedback or 'continue' to proceed: ").strip()
        
        if not feedback:
            warning("Input was empty. Please provide feedback or type 'continue'.")
            continue
        
        if feedback.lower() == "continue":
            return "continue", base_query
        else:
            updated_query = f"""Parent query: {base_query}

Previous generated schema:
{fields.generated_schema}

Suggestion from the user:
{feedback}
"""
            return feedback, updated_query

async def run_and_save(file_bytes, filename, system_prompt):
    status("Generating dataset rows...")
    dataset_rows = None

    async for message in generate_full_dataset(file_bytes, filename, system_prompt):
        if message.startswith("data:__DONE__:"):
            data_str = message[len("data:__DONE__:"):]
            data_json = json.loads(data_str)
            dataset_rows = data_json['rows']
            break
        else:
            print(message.strip())

    if dataset_rows:
        # Create filename based on current date & time
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_filename = f"final_dataset_{timestamp}.json"

        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(dataset_rows, f, indent=2, ensure_ascii=False)

        success(f"Dataset saved to '{output_filename}'.")
    else:
        error("Dataset generation failed or returned empty.")

def main():
    render_banner()

    file_path = Prompt.ask("[bold yellow]Enter the file path[/bold yellow]").strip()
    base_query = Prompt.ask("[bold yellow]Enter additional instruction and information about the file source[/bold yellow]").strip()

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    current_query = base_query
    feedback = None

    # Feedback loop
    while feedback != "continue":
        fields = generate_dataset_schema(current_query)
        feedback, current_query = get_user_feedback(fields, base_query)

    # Generate dataset
    system_prompt = process_datagen_prompt(fields.generated_schema)
    asyncio.run(run_and_save(file_bytes, file_path, system_prompt))

if __name__ == "__main__":
    main()

