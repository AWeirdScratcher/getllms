import re
import sys

from holdon.escapes import CURSOR, ERASE
from holdon.progress import human_readable_bytes

from .core import get_model, list_models
from .model import ModelFile


def main():
    if not sys.argv[1:]:
        help_fn()

    command = sys.argv[1]

    if command == "list":
        list_fn()
    elif command == "download":
        download_fn(2)
    else:
        download_fn()

def bold(t: str):
    return "\033[1m%s\033[0m" % t

def blue(t: str):
    return "\033[0;34m%s\033[0m" % t

def red(t: str):
    return "\033[0;31m%s\033[0m" % t

def dark(t: str):
    return "\033[2m%s\033[0m" % t

def underline(t: str):
    return "\033[4m%s\033[0m" % t

def help_fn(_exit: bool = True):
    model_arg = f"{red('<model name>')} | {red('<name[economical | best]>')}"
    print(f"""
{bold('getllms')} {model_arg} - Download a model.

Commands:
    {dark('getllms')} {blue('list')} - List all available models.
    {dark('getllms')} {blue('download')} {model_arg} - Download a model.
""")
    if _exit:
        exit()

def list_fn():
    print(f"\n{red('getllms')} models\n\n")
    tr = sys.argv[2] if len(sys.argv) >= 3 else "null"
    truncate = None if tr == "all" else 5

    for model in list_models()[:truncate]:
        print(blue(underline(model.name)) + "\n\n" + model.description + "\n\n")

    if truncate:
        print(dark("truncated to 5 models. use `getllms list all` to list all.\n"))

def download_fn(level: int = 1):
    model_name = sys.argv[level] if len(sys.argv) >= level + 1 else None

    if not model_name:
        help_fn(False)
        print(red("download: missing argument <model name>\n"))
        exit(1)

    matches = re.findall(r"^(.+?)\s*\[(.+)\]$", model_name)

    if not matches:
        name = model_name
        type_ = "economical"
    else:
        name = matches[0][0]
        type_ = matches[0][1]

        if type_ not in {"economical", "best"}:
            print(red("model (file) type should be 'economical' or 'best'"))
            exit(1)

    try:
        model = get_model(name)
    except KeyError:
        print(red(f"Cannot find model {model_name!r}"))
        exit(1)

    file: ModelFile = getattr(model.files, type_)
    print(f"\n{blue('[getllms]')} {bold(name)} {dark(f'({type_})')}")
    print(
        blue("[getllms] ") + 
        red(
            "size: " + human_readable_bytes(file.size)
        )
    )
    input(
        blue("[getllms] ") + "enter to continue"
    )
    print(CURSOR.prev_line_begin() + ERASE.ENTIRE_LINE)

    model.download(
        sys.argv[level + 1] if len(sys.argv) >= level + 2 else None,
        type=type_
    )
