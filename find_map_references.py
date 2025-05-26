import os
import re
from pathlib import Path

def find_map_references(static_root):
    """
    Scan all files in static folder for .map references
    Returns: {file_path: [list_of_referenced_map_files]}
    """
    map_references = {}
    # Regex to match both JS and CSS sourcemap declarations
    pattern = re.compile(r'//# sourceMappingURL=(.*\.map)|/\*# sourceMappingURL=(.*\.map)')

    for root, _, files in os.walk(static_root):
        for file in files:
            # Check only JS/CSS files
            if not file.endswith(('.js', '.css')):
                continue

            file_path = Path(root) / file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = pattern.finditer(content)
                    
                    for match in matches:
                        # Extract the .map filename (handles both JS and CSS syntax)
                        map_file = match.group(1) or match.group(2)
                        if file_path not in map_references:
                            map_references[file_path] = []
                        map_references[file_path].append(map_file)
                        
            except (UnicodeDecodeError, PermissionError):
                continue

    return map_references

if __name__ == "__main__":
    STATIC_ROOT = "static"  # Your static folder path (update if different)
    
    print(f"🔍 Scanning {STATIC_ROOT} for .map references...")
    references = find_map_references(STATIC_ROOT)
    
    if references:
        print("\n🚨 Found references to .map files in:")
        for file, maps in references.items():
            print(f"\n📄 {file}:")
            for map_file in maps:
                print(f"   → {map_file}")
        print(f"\nTotal references found: {sum(len(v) for v in references.values())}")
    else:
        print("\n✅ No .map file references found in static files")


def remove_map_references(file_path):
    """Remove all sourcemap references from a file"""
    pattern = re.compile(r'(//# sourceMappingURL=|/\*# sourceMappingURL=)(.*\.map)')
    try:
        with open(file_path, 'r+', encoding='utf-8') as f:
            content = f.read()
            new_content = pattern.sub('', content)
            if content != new_content:
                f.seek(0)
                f.write(new_content)
                f.truncate()
                return True
    except (UnicodeDecodeError, PermissionError):
        return False
    return False

if references:
    for file in references.keys():
        if remove_map_references(file):
            print(f"✔️ Cleaned {file}")



