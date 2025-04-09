import os
import glob
import shutil
from utils.utils import Utils

class ItemsAdder:
    def __init__(self):
        self.armors_rendering = {}
        self.furnace_data = {"items": {}}
        self.item_ids = Utils.load_yaml("ItemsAdder/storage/items_ids_cache.yml")

    def extract(self):
        os.makedirs("output/itemsadder", exist_ok=True)
        datas = [Utils.load_yaml(file) for file in glob.glob("ItemsAdder/contents/**/*.yml", recursive=True)]
        self.armors_rendering.update({k: v for data in datas for k, v in data.get("armors_rendering", {}).items()})

        for data in datas:
            if not "items" in data:
                continue

            namespace = data["info"]["namespace"]
            for item_id, item_data in data["items"].items():
                if not item_data: continue
                armor_data = item_data.get("specific_properties", {}).get("armor", {})
                if not armor_data.get("slot") or armor_data.get("custom_armor") not in self.armors_rendering:
                    continue
                slot = armor_data["slot"]
                layer = "layer_2" if slot == "legs" else "layer_1"
                layer_rendering = self.armors_rendering[armor_data["custom_armor"]]
                armor_type = {
                    "head": "HELMET",
                    "chest": "CHESTPLATE",
                    "legs": "LEGGINGS",
                    "feet": "BOOTS"
                }[slot.lower()]
                material = item_data["resource"].get("material", f"LEATHER_{armor_type}")

                item_key = f"{namespace}:{item_id}"
                if item_key not in self.item_ids.get(material, {}):
                    print(f"Not found: {item_key} {material}")
                    continue

                custom_model_data = str(self.item_ids[material][f"{namespace}:{item_id}"])
                files = glob.glob(f"ItemsAdder/contents/**/textures/{layer_rendering[layer]}.png", recursive=True)
                if len(files) == 0: continue
                file = files[0]
                
                os.makedirs(os.path.dirname(f"output/itemsadder/textures/models/{layer_rendering[layer]}.png"), exist_ok=True)
                shutil.copy(file, f"output/itemsadder/textures/models/{layer_rendering[layer]}.png")

                self.furnace_data["items"].setdefault(f"minecraft:{material}".lower(), {}).setdefault("custom_model_data", {})[custom_model_data] = {
                    "armor_layer": {
                        "type": armor_type.lower(),
                        "texture": f"textures/models/{layer_rendering[layer]}",
                        "auto_copy_texture": False
                    }
                }

        Utils.save_json("output/itemsadder/furnace.json", self.furnace_data)