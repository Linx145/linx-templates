import importlib
from pathlib import Path
import subprocess
import sys
import io
import os
import shutil

def copy_overwrite(src, dest, debug_print=False):
    dest_dir = os.path.dirname(dest)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    if os.path.exists(dest):
        os.remove(dest)
    shutil.copy2(src, dest)
    if debug_print:
        print(f"{src} copied to {dest}")

def install_and_import(package):
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"{package} not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[package] = importlib.import_module(package)

install_and_import("requests")
install_and_import("urllib")
install_and_import("zipfile")

def download_bytes_url(url):
    try:
        print(f"Downloading bytes from {url}")
        response = requests.get(url, stream=True) # type: ignore
        response.raise_for_status()

        return io.BytesIO(response.content)
    except requests.exceptions.RequestException as e: # type: ignore
        print(f"RequestException: Error downloading from {url}: {e}")
        return None
    except Exception as e:
        print(f"Exception: Error downloading from {url}: {e}")
        return None

def download_file_url(url, dir):
    try:
        print(f"Downloading file from {url}")
        response = requests.get(url, stream=True) # type: ignore
        response.raise_for_status()

        parsed_url = urllib.parse.urlparse(url) # type: ignore
        filename = os.path.basename(parsed_url.path)

        filepath = os.path.join(dir, filename)
        os.makedirs(dir, exist_ok=True)

        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        return filepath 
    except requests.exceptions.RequestException as e: # type: ignore
        print(f"RequestException: Error downloading from {url}: {e}")
        return None 
    except Exception as e:
        print(f"Exception: Error downloading from {url}: {e}")
        return None 


def extract_zip_bytes(bytes, dir):
    if bytes == None:
        return False 
    try:
        with zipfile.ZipFile(bytes) as zip: # type: ignore
            zip.extractall(dir)
        return True
    except zipfile.BadZipFile: # type: ignore
        print("Invalid zip file")
        return False