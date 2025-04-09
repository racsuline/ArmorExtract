import os
import requests
from zipfile import ZipFile

class Loader:
    def load(input_content: str, output: str = ".") -> None:
        print("Loading files...")
        if input_content.startswith("http"):
            with requests.get(Loader.get_link_download(input_content), headers={'User-Agent': 'Mozilla/5.0'}, stream=True, allow_redirects=True) as r:
                with open("Content.zip", "wb") as f: f.write(r.content)
            filepack = f"Content.zip"
        elif input_content.endswith(".zip"):
            filepack = input_content
        if not (os.path.isfile(filepack) and Loader.is_zip_file(filepack)):
            raise FileNotFoundError("Not found or not a valid zip file.")
        with ZipFile(filepack) as z:
            if not any(n.startswith(("ItemsAdder", "Nexo")) for n in z.namelist()):
                raise ValueError("Zip missing ItemsAdder or Nexo.")
            z.extractall(output)
        print("Loaded files")
    
    @staticmethod
    def get_link_download(link: str) -> str:
        if link.startswith("https://www.dropbox.com"):
            return link.replace("dl=0", "dl=1")
        return link

    @staticmethod
    def is_zip_file(file_path: str) -> bool:
        with open(file_path, 'rb') as file:
            header = file.read(4)
            return header == b'PK\x03\x04'
    