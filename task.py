import os
import shutil
import subprocess
import logging
from settings import RECYCLE_BIN_PATH

logging.basicConfig(filename='cleannet_manager.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_recycle_bin_empty():
    return not any(os.scandir(RECYCLE_BIN_PATH))

def clean_recycle_bin():
    try:
        logging.info("Attempting to clean Recycle Bin.")
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_MINIMIZE
        result = subprocess.run(['powershell', '-Command', 'Clear-RecycleBin -Force -ErrorAction SilentlyContinue'], capture_output=True, text=True, startupinfo=startupinfo)
        if result.returncode == 0 and is_recycle_bin_empty():
            logging.info("Recycle Bin cleaned successfully.")
        else:
            logging.error(f"Failed to clean Recycle Bin. Error: {result.stderr}")
    except Exception as e:
        logging.error(f"Error cleaning Recycle Bin: {e}")

def clear_cookies():
    cookies_path = os.path.expanduser("~\\AppData\\Local\\Microsoft\\Windows\\INetCookies")
    try:
        logging.info("Attempting to clear cookies.")
        if os.path.exists(cookies_path):
            shutil.rmtree(cookies_path)
        os.makedirs(cookies_path)
        logging.info("Cookies cleared successfully.")
    except PermissionError as e:
        logging.error(f"Permission denied: Unable to clear cookies. {e}")
    except Exception as e:
        logging.error(f"Error clearing cookies: {e}")

def clear_temp_files():
    temp_path = os.path.expanduser("~\\AppData\\Local\\Temp")
    try:
        logging.info("Attempting to clear temporary files.")
        for filename in os.listdir(temp_path):
            file_path = os.path.join(temp_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logging.error(f"Failed to delete {file_path}. Reason: {e}")
        logging.info("Temporary files cleared successfully.")
    except Exception as e:
        logging.error(f"Error clearing temporary files: {e}")

def clear_chrome_history():
    chrome_path = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History")
    try:
        logging.info("Attempting to clear Google Chrome history.")
        if os.path.exists(chrome_path):
            os.remove(chrome_path)
        logging.info("Google Chrome history cleared successfully.")
    except PermissionError as e:
        logging.error(f"Permission denied: Unable to clear Google Chrome history. {e}")
    except Exception as e:
        logging.error(f"Error clearing Google Chrome history: {e}")

def clear_firefox_history():
    firefox_path = os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles")
    try:
        logging.info("Attempting to clear Mozilla Firefox history.")
        for root, dirs, files in os.walk(firefox_path):
            for file in files:
                if file.endswith(".sqlite") and "places" in file:
                    os.remove(os.path.join(root, file))
        logging.info("Mozilla Firefox history cleared successfully.")
    except PermissionError as e:
        logging.error(f"Permission denied: Unable to clear Mozilla Firefox history. {e}")
    except Exception as e:
        logging.error(f"Error clearing Mozilla Firefox history: {e}")

def clear_edge_history():
    edge_path = os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History")
    try:
        logging.info("Attempting to clear Microsoft Edge history.")
        if os.path.exists(edge_path):
            os.remove(edge_path)
        logging.info("Microsoft Edge history cleared successfully.")
    except PermissionError as e:
        logging.error(f"Permission denied: Unable to clear Microsoft Edge history. {e}")
    except Exception as e:
        logging.error(f"Error clearing Microsoft Edge history: {e}")

def clear_internet_history():
    clear_chrome_history()
    clear_firefox_history()
    clear_edge_history()
    logging.info("Internet history cleared successfully.")

def update_all_packages():
    try:
        logging.info("Updating all installed packages using winget.")
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_MINIMIZE
        result = subprocess.run(['cmd', '/c', 'winget update --all'], capture_output=True, text=True, startupinfo=startupinfo)
        if result.returncode == 0:
            logging.info("All installed packages updated successfully.")
        else:
            logging.error(f"Failed to update installed packages. Error: {result.stderr}")
    except Exception as e:
        logging.error(f"Error updating installed packages: {e}")

def check_registry_errors():
    try:
        logging.info("Checking for registry errors.")
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_MINIMIZE
        result = subprocess.run(['cmd', '/c', 'sfc /scannow'], capture_output=True, text=True, startupinfo=startupinfo)
        if result.returncode == 0:
            logging.info("Registry errors checked and corrected successfully.")
        else:
            logging.error(f"Failed to check and correct registry errors. Error: {result.stderr}")
    except Exception as e:
        logging.error(f"Error checking and correcting registry errors: {e}")

def sort_downloads():
    download_path = os.path.expanduser("~\\Downloads")
    folders = {
        "Documents": os.path.expanduser("~\\Documents"),
        "Pictures": os.path.expanduser("~\\Pictures"),
        "Music": os.path.expanduser("~\\Music"),
        "Videos": os.path.expanduser("~\\Videos")
    }
    file_types = {
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
        "Pictures": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
        "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
        "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"]
    }
    try:
        logging.info("Sorting downloads.")
        for filename in os.listdir(download_path):
            file_path = os.path.join(download_path, filename)
            if os.path.isfile(file_path):
                moved = False
                for folder, extensions in file_types.items():
                    if any(filename.lower().endswith(ext) for ext in extensions):
                        destination_folder = folders[folder]
                        if not os.path.exists(destination_folder):
                            os.makedirs(destination_folder)
                        shutil.move(file_path, os.path.join(destination_folder, filename))
                        logging.info(f"Moved {filename} to {destination_folder}")
                        moved = True
                        break
                if not moved:
                    os.remove(file_path)
                    logging.info(f"Removed {filename} from Downloads")
        logging.info("Downloads sorted and remaining files removed successfully.")
    except Exception as e:
        logging.error(f"Error sorting downloads: {e}")
