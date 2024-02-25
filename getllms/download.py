from __future__ import annotations

import requests
from holdon import progress

def download(url: str, to: str):
    """Download a file.
    
    Args:
        url (str): The URL.
        to (str): File location.
    """
    r = requests.get(url, stream=True)
    size = int(r.headers['Content-Length'])

    with open(to, "wb") as f:
        for chunk in progress(
            r.iter_content(chunk_size=4096 * 5), 
            size=size, 
            unit="bytes"
        ):
            f.write(chunk)

    print("Downloaded.")
