from rich.console import Console
from rich.pretty import Pretty
from rich.markdown import Markdown


console = Console(width=80)

def my_print(value, *, markup: bool = False, markdown: bool = False):
    if isinstance(value, str):
        if markdown:
            console.print(Markdown(value))
        else:
            console.print(value, markup=markup)
    else:
        console.print(
            Pretty(
                value,
                overflow="fold",
                no_wrap=False,
                indent_guides=True,
                expand_all=True,
            ),
            soft_wrap=False,
        )