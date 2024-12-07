import time

from rich.text import Text
from rich.console import Console
from rich.live import Live

# text = Text("Hello, [bold magenta]World[/bold magenta]!")

# print(text)

# time.sleep(2)

# text = Text("Hello, [bold red]World[/bold red]!")
# print(text)

# time.sleep(4)


def scroll_text(text, width=40, delay=1):
    console = Console()
    t = ["line 1", "line 2", "line 3", "line 4", "line 5", "line 6", "line 7"]
    with Live(console=console, refresh_per_second=10) as live:
        for i in range(len(t)):
            visible_text = t[i]
            live.update(Text(visible_text))
            time.sleep(delay)


scroll_text(
    "This is a scrolling text example using the rich library. ", width=40, delay=0.1
)
