import urllib.request


def download_file(url: str, file_name: str) -> None:
    urllib.request.urlretrieve(url, file_name)
