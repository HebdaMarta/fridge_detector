import kagglehub
import shutil
import os

path = kagglehub.dataset_download("crispen5gar/recipes3k")

target_dir = "data"
os.makedirs(target_dir, exist_ok=True)

files = os.listdir(path)
for file in files:
    if file.endswith(".json"):
        source_file = os.path.join(path, file)
        destination_file = os.path.join(target_dir, "recipes.json")
        shutil.copy2(source_file, destination_file)
        print(f"Plik skopiowany do: {destination_file}")
        break
else:
    print("Nie znaleziono pliku JSON w pobranym datasecie.")