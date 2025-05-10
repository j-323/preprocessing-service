import typer
from src.core.agent import PreprocessingAgent

app = typer.Typer(help="CLI for Song Preprocessor Agent")

@app.command()
def preprocess(track_id: int, file: str):
    text = open(file, encoding="utf-8").read()
    agent = PreprocessingAgent()
    resp = agent.run_sync(track_id, text)
    typer.echo(resp.json())

if __name__ == "__main__":
    app()