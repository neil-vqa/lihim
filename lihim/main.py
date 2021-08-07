import typer

app = typer.Typer()

group_list = ['aws','azure','gcp']

@app.command()
def groups():
    typer.echo(print_groups())

@app.command()
def notes():
    typer.echo(group_list)

def print_groups():
    for group in group_list:
        print(group)

def main():
    pass

if __name__ == "__main__":
    app()