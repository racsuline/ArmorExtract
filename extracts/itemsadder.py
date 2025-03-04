import os
import json
import glob
import shutil
from utils import Utils

class ItemsAdder:
    def __init__(self):
        self.armors_rendering = {}
        self.furnace_data = {"items": {}}
        self.item_ids = Utils.load_yaml("ItemsAdder/storage/items_ids_cache.yml")

    def extract(self):
        os.makedirs("output/itemsadder", exist_ok=True)
        try:
            datas = [Utils.load_yaml(file) for file in glob.glob("ItemsAdder/contents/**/*.yml", recursive=True)]
        except Exception as e:
            raise Exception(f"Error loading YAML files: {str(e)}")
            
        self.armors_rendering.update({k: v for data in datas for k, v in data.get("armors_rendering", {}).items()})

        for data in datas:
            if "items" not in data:
                continue

            namespace = data["info"]["namespace"]
            for item_id, item_data in data["items"].items():
                if "specific_properties" not in item_data or "armor" not in item_data["specific_properties"] or "slot" not in item_data["specific_properties"]["armor"] or "custom_armor" not in item_data["specific_properties"]["armor"]:
                    continue
                if item_data["specific_properties"]["armor"]["custom_armor"] not in self.armors_rendering:
                    continue
                slot = item_data["specific_properties"]["armor"]["slot"]
                layer = "layer_2" if slot == "legs" else "layer_1"
                layer_rendering = self.armors_rendering[item_data["specific_properties"]["armor"]["custom_armor"]]
                armor_type = {
                    "head": "HELMET",
                    "chest": "CHESTPLATE",
                    "legs": "LEGGINGS",
                    "feet": "BOOTS"
                }[slot.lower()]
                material = item_data["resource"].get("material", f"LEATHER_{armor_type}")
                custom_model_data = str(self.item_ids[material][f"{namespace}:{item_id}"])

                search_paths = [
                    f"ItemsAdder/contents/**/textures/{layer_rendering[layer]}.png",
                    f"ItemsAdder/contents/**/textures/armor/{layer_rendering[layer]}.png",
                    f"ItemsAdder/contents/**/resourcepack/assets/**/textures/{layer_rendering[layer]}.png"
                ]

                file = None
                for path in search_paths:
                    try:
                        files = glob.glob(path, recursive=True)
                        if files:
                            file = files[0]
                            break
                    except Exception as e:
                        raise Exception(f"Error searching for texture files in {path}: {str(e)}")

                if file:
                    try:
                        os.makedirs(os.path.dirname(f"output/itemsadder/textures/models/{layer_rendering[layer]}.png"), exist_ok=True)
                        shutil.copy(file, f"output/itemsadder/textures/models/{layer_rendering[layer]}.png")
                    except Exception as e:
                        raise Exception(f"Error copying texture file {file}: {str(e)}")

                    self.furnace_data["items"].setdefault(f"minecraft:{material}".lower(), {}).setdefault("custom_model_data", {})[custom_model_data] = {
                        "armor_layer": {
                            "type": armor_type.lower(),
                            "texture": f"textures/models/{layer_rendering[layer]}",
                            "auto_copy_texture": False
                        }
                    }
                else:
                    raise Exception(f"Texture file not found for {layer_rendering[layer]} in any of the search paths")

        try:
            Utils.save_json("output/itemsadder/furnace.json", self.furnace_data)
        except Exception as e:
            raise Exception(f"Error saving furnace.json: {str(e)}")
