import os
import re
from pathlib import Path
import sys

def safe_resolve(path):
    """Handle long paths on Windows with fallback"""
    try:
        return path.resolve()
    except (OSError, ValueError):
        # Fallback for Windows path length limitations
        return Path(os.path.abspath(str(path)))

def find_missing_images(static_root):
    """
    Scan all files in static folder for missing image references
    Returns: {file_path: [list_of_missing_images]}
    """
    missing_images = {}
    static_path = safe_resolve(Path(static_root))
    
    # Regex patterns to match image references
    patterns = [
        re.compile(r'url\([\'"]?(.*?\.(?:png|jpg|jpeg|gif|svg|webp))[\'"]?\)', re.I),  # CSS
        re.compile(r'[\'"]src[\'"]\s*:\s*[\'"](.*?\.(?:png|jpg|jpeg|gif|svg|webp))[\'"]', re.I),  # JS
        re.compile(r'<img[^>]+src=[\'"](.*?\.(?:png|jpg|jpeg|gif|svg|webp))[\'"]', re.I),  # HTML
    ]

    for root, _, files in os.walk(str(static_path)):
        for file in files:
            if not file.endswith(('.css', '.js', '.html')):
                continue

            file_path = safe_resolve(Path(root) / file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    for pattern in patterns:
                        for match in pattern.finditer(content):
                            img_ref = match.group(1)
                            
                            # Skip external resources
                            if img_ref.startswith(('http://', 'https://', 'data:')):
                                continue
                            
                            # Handle different path formats
                            if img_ref.startswith('/'):
                                abs_img_path = static_path / img_ref.lstrip('/')
                            else:
                                abs_img_path = safe_resolve(file_path.parent / img_ref)
                            
                            # Check if exists (with Windows long path workaround)
                            try:
                                if not abs_img_path.exists():
                                    missing_images.setdefault(str(file_path), []).append(img_ref)
                            except OSError:
                                missing_images.setdefault(str(file_path), []).append(f"[PATH ERROR] {img_ref}")

            except (UnicodeDecodeError, PermissionError) as e:
                print(f"⚠️ Skipping {file_path}: {str(e)}", file=sys.stderr)
                continue

    return missing_images

def print_report(missing_data):
    if not missing_data:
        print("\n✅ No missing image references found!")
        return
        
    print("\n🚨 Missing image references found:")
    total = 0
    for file, images in missing_data.items():
        print(f"\n📄 {file} references:")
        for img in images:
            print(f"   → {img}")
            total += 1
    print(f"\nTotal missing references: {total}")

if __name__ == "__main__":
    # Automatically detect static folder at project root
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    STATIC_ROOT = PROJECT_ROOT / "static"
    
    print(f"🔍 Scanning {STATIC_ROOT} for missing image references...")
    missing = find_missing_images(STATIC_ROOT)
    print_report(missing)