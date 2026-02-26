import click
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

# Initialize OpenAI client
client = OpenAI()
console = Console()

@click.command()
@click.argument('log_path', type=click.Path(exists=True))
def log_analyze(log_path):
    """AI-powered log analyzer for identifying errors and patterns."""
    with open(log_path, 'r') as f:
        logs = f.read()

    console.print(f"[bold blue]Analyzing logs from {log_path}...[/bold blue]")

    prompt = f"""
    Analyze the following log entries and identify errors, warnings, unusual patterns, and provide a summary of findings.
    Format your response in Markdown.

    Logs:
    ```
    {logs}
    ```
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {{"role": "system", "content": "You are an expert system administrator."}},
                {{"role": "user", "content": prompt}}
            ]
        )
        analysis_text = response.choices[0].message.content
        console.print(Markdown(analysis_text))
    except Exception as e:
        console.print(f"[bold red]Error during log analysis:[/bold red] {e}")

if __name__ == '__main__':
    log_analyze()
