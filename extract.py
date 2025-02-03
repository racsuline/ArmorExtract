from extracts.itemsadder import ItemsAdder
import os

if all(os.path.exists(path) for path in ("ItemsAdder/contents", "ItemsAdder/storage/items_ids_cache.yml")):
    ItemsAdder().extract()