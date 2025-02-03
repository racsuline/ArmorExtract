# Auto Armor Generator For Furnace
This tool allows you automatically generate armor from itemsadder,... for furnace.

## How to use
### Local
1. Install Python
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Upload content from ItemsAdder / Nexo / ...
- ItemsAdder: zip `content` folder and `storage` folder with `items_ids_cache.yml`. Rename zip to `Content.zip`
- Nexo: 🏗
4. Run script
```bash
python extract.py
```

### Github Action
1. Fork / Import to New Repository
2. Upload content from ItemsAdder / Nexo / ... to download link
- ItemsAdder: zip `content` folder and `storage` folder with `items_ids_cache.yml`. Rename zip to `Content.zip`
- Nexo: 🏗
3. Go to Actions -> Extract Armors -> Run workflow -> Input Download URL -> Run
4. Wait for the job to finish and download artifact