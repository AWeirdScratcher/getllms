import os
import time

import requests


def readable_bytes(size, decimal_places=2):
    for unit in ('B', 'KB', 'MB', 'GB'):
        if size < 1024.0:
            return f"{size:.{decimal_places}f}{unit}"

        size /= 1024.0
    return f"{size:.{decimal_places}f}TB"

def in_notebook() -> bool:
    """Is this running in a notebook?

    .. note ::

        See https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook

    Returns:
        bool: The result.
    """
    try:
        from IPython import get_ipython # type: ignore

        if 'IPKernelApp' not in get_ipython().config: # type: ignore
            return False

    except ImportError:
        return False

    except AttributeError:
        return False

    return True


def unsafe_download(*, url: str, to: str, nb: bool):
    """Download function without KeyboardInterrupt handling.

    It's recommend to use the ``download()`` function instead.

    Args:
        url (str): The target URL. Uses GET request.
        to (str): The destination as a file.
        nb (bool): In a notebook?
    """
    t = "Downloading... "
    r = requests.get(url, stream=True)
    r.raise_for_status()
    full = int(r.headers['Content-Length'])
    rdb_full = readable_bytes(full)
    curr = 0
    rdb_curr = readable_bytes(curr)
    prev_t = t + f"{rdb_curr} / {rdb_full}"

    def render(*, initial: bool=False):
        nonlocal rdb_curr, prev_t
        rdb_curr = readable_bytes(curr)

        if nb:
            this_t = (
                t +
                f"{((curr/full) * 100):.2f}%"
            )
            print(
                ("" if initial else "\r") + 
                this_t + " " * abs(len(this_t) - len(prev_t))
            )

        else:
            this_t = (
                t +
                f"{rdb_curr} / {rdb_full} "
                f"\033[2m({((curr/full) * 100):.2f}%)\033[0m"
            )
            print(
                "" if initial else "\r" + this_t + " " * (
                    os.get_terminal_size().columns - len(this_t) - 1
                ),
                end=""
            )

        prev_t = this_t

    if not nb:
        print("\033[?25l", end="")

    render(initial=True)

    s = time.time()
    with open(to, "wb") as f:
        for chunk in r.iter_content(4096 * 4):
            f.write(chunk)
            curr += len(chunk)
            render()

    print(
        f"\nDownloaded. {(time.time() - s):.3f}s" +
        "" if nb else "\033[?25h"
    )


def download(*, url: str, to: str):
    """Download a file from the Internet.

    Args:
        url (str): The target URL. Uses GET request.
        to (str): The destination as a file.

    Example:
        .. code-block :: python

            download(
                url="https://example.com/robots.txt",
                to="robots.txt"
            )
    """
    nb = in_notebook()

    try:
        unsafe_download(url=url, to=to, nb=nb)

    except KeyboardInterrupt as err:
        if not nb:
            print("\033[?25h", end="")
        raise err
