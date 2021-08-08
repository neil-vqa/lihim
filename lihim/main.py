from typing import List
import typer

app = typer.Typer()

user_list = ['neeban','neil']
group_list = ['aws','azure','gcp']

@app.command()
def users():
    typer.echo(print_list(user_list))

@app.command()
def groups():
    typer.echo(print_list(group_list))


def print_list(list_type: List[str]):
    for item in list_type:
        print(item)

def main():
    pass

if __name__ == "__main__":
    app()