import json, os, datetime

MEMORY_FILE = "memory.json"
GLYPH_FILE = "glyphs.json"
SEED_FOLDER = "seeds/"
REFLECT_FOLDER = "reflections/"

def load_glyphs():
    with open(GLYPH_FILE, "r") as f:
        return json.load(f)

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def store_memory(entry):
    memory = load_memory()
    memory.append(entry)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def parse_seed(file_path, glyphs):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    used = [g for g in glyphs if g in content]
    meaning = [glyphs[g]["meaning"] for g in used]
    return {
        "file": file_path,
        "used_glyphs": used,
        "decoded_meaning": meaning,
        "timestamp": str(datetime.datetime.utcnow())
    }

def reflect(seed_data):
    out = f"# Reflection on {seed_data['file']}\n"
    out += f"Used Glyphs: {', '.join(seed_data['used_glyphs'])}\n"
    out += "Meanings:\n"
    for m in seed_data['decoded_meaning']:
        out += f"- {m}\n"
    return out

def main():
    glyphs = load_glyphs()
    for seed_file in os.listdir(SEED_FOLDER):
        if seed_file.endswith(".md") or seed_file.endswith(".yaml"):
            data = parse_seed(SEED_FOLDER + seed_file, glyphs)
            output = reflect(data)
            out_file = f"{REFLECT_FOLDER}/reflection_{seed_file.replace('.', '_')}.txt"
            with open(out_file, "w") as f:
                f.write(output)
            store_memory(data)

if __name__ == "__main__":
    main()

