import typer
from lib.agent import agent_executor

app = typer.Typer()


@app.command()
def ext(user_input: str, pdf: bool = typer.Option(False, help="Flag to specify extracting from a PDF document")):
    if pdf:
        print("scan PDF")
    else:
        print(agent_executor.run(user_input))


if __name__ == "__main__":
    app()
