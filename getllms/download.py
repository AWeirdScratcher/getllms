import os
import time

import requests


def readable_bytes(size, decimal_places=2):
    for unit in ('B', 'KB', 'MB', 'GB'):
        if size < 1024.0:
            return f"{size:.{decimal_places}f}{unit}"

        size /= 1024.0
    return f"{size:.{decimal_places}f}TB"

def unsafe_download(*, url: str, to: str):
    """Download function without KeyboardInterrupt handling.

    It's recommend to use the ``download()`` function instead.

    Args:
        url (str): The target URL. Uses GET request.
        to (str): The destination as a file.
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

    print("\033[?25l", end="")
    render(initial=True)

    s = time.time()
    with open(to, "wb") as f:
        for chunk in r.iter_content(4096 * 4):
            f.write(chunk)
            curr += len(chunk)
            render()

    print(
        f"\nDownloaded. {(time.time() - s):.3f}s\033[?25h"
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
    try:
        unsafe_download(url=url, to=to)
    except KeyboardInterrupt as err:
        print("\033[?25h", end="")
        raise err
