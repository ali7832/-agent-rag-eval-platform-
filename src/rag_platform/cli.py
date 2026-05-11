import typer
from rich import print

app = typer.Typer(help="Agent RAG Evaluation Platform CLI")


@app.command()
def ingest(path: str) -> None:
    print(f"[green]Ingesting documents from:[/green] {path}")


@app.command()
def search(query: str) -> None:
    print(f"[cyan]Searching:[/cyan] {query}")


@app.command()
def query(question: str) -> None:
    print(f"[yellow]Question:[/yellow] {question}")
    print("Grounded placeholder answer.")


if __name__ == "__main__":
    app()
