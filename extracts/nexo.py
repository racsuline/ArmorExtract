import os
import glob
import shutil
from zipfile import ZipFile
from utils.utils import Utils

class Nexo:
    def __init__(self):
        self.furnace_data = {"items": {}}
        self.armor_types = ["HELMET", "CHESTPLATE", "LEGGINGS", "BOOTS"]

    def extract(self):
        os.makedirs("output/nexo", exist_ok=True)
        with ZipFile("Nexo/pack/pack.zip") as z: z.extractall("Nexo/pack")
        data_files = glob.glob("Nexo/items/**/*.yml", recursive=True)
        for file in data_files:
            data = Utils.load_yaml(file)
            for item_id, item in data.items():
                material = item.get("material", "")
                model_id = item.get("Pack", {}).get("custom_model_data")
                if not model_id or not any(t in material for t in self.armor_types): continue
                textures = item.get("Pack", {}).get("textures") or [item.get("Pack", {}).get("texture")]
                textures = [t for t in textures if t]
                for tex in textures:
                    armor_type = self.get_armor_type(material).lower()
                    texture_path = self.build_texture_path(tex, armor_type)
                    full_src = os.path.join("Nexo/pack/assets", texture_path)
                    if not os.path.exists(full_src):
                        full_src = self.find_alternative_path(texture_path)
                        if not full_src:
                            print(f"Missing texture: {texture_path}")
                            continue
                        texture_path = os.path.relpath(full_src, "Nexo/pack/assets").replace("\\", "/")

                    dst_path = os.path.join("output/nexo/textures/models", texture_path)
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    shutil.copy(full_src, dst_path)

                    self.furnace_data["items"].setdefault(f"minecraft:{material}".lower(), {}).setdefault("custom_model_data", {})[model_id] = {
                        "armor_layer": {
                            "type": armor_type,
                            "texture": f"textures/models/{texture_path}",
                            "auto_copy_texture": False
                        }
                    }

        Utils.save_json("output/nexo/furnace.json", self.furnace_data)

    def get_armor_type(self, material: str) -> str:
        return next((t for t in self.armor_types if t in material), "UNKNOWN")

    def build_texture_path(self, tex: str, armor_type: str) -> str:
        base = tex.replace(":", "/textures/") if ":" in tex else f"minecraft/textures/{tex}"
        layer = "layer_2" if "leggings" in armor_type else "layer_1"
        prefix = os.path.basename(base).split("_")[0]
        return f"{os.path.dirname(base)}/{prefix}_armor_{layer}.png"

    def find_alternative_path(self, original_path: str) -> str | None:
        base = os.path.basename(original_path)
        pattern = f"{os.path.dirname(original_path)}/{base.split('_')[0]}**_{base.split('_', 1)[-1]}"
        matches = glob.glob(f"Nexo/pack/assets/{pattern}", recursive=True)
        return matches[0] if matches else None