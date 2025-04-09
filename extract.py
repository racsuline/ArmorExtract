from extracts.itemsadder import ItemsAdder
from extracts.nexo import Nexo
from utils.loader import Loader 
from utils.utils import Utils
import os

if os.path.exists(".env"):
    import dotenv
    dotenv.load_dotenv()

Utils.clear_old_convert("ItemsAdder", "Nexo", "output")

try:
    Loader.load(os.getenv("input_content"))
    if all(os.path.exists(path) for path in ("ItemsAdder/contents", "ItemsAdder/storage/items_ids_cache.yml")):
        ItemsAdder().extract()
    if all(os.path.exists(path) for path in ("Nexo/items", "Nexo/pack/pack.zip")):
        Nexo().extract()
    print("Done")
except Exception as e:
    print(f"Error loading: {e}")