import argparse
import shutil
from pathlib import Path
import json

VAULT_DIR = Path.home() / ".dtx"
REGISTRY_FILE = VAULT_DIR / "dtx.json"

def load_registry():
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_registry(data):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def init_vault():
    if VAULT_DIR.exists():
        print(f"Vault already exists at: {VAULT_DIR}")
    else:
        VAULT_DIR.mkdir(parents=True)
        print(f"Initialized empty vault at: {VAULT_DIR}")

def add_file(filepath):
    source_path = Path(filepath).resolve()
    
    if not source_path.exists() or not source_path.is_file():
        print(f"Error: '{source_path}' does not exist or is not a regular file.")
        return

    if not VAULT_DIR.exists():
        print("Error: Vault is not initialized. Run 'dtx init' first.")
        return

    path = VAULT_DIR / source_path.name
    if path.exists():
        print(f"Error: '{source_path.name}' is already tracked in the vault.")
        return

    shutil.move(str(source_path), str(path))
    print(f"Moved to vault: {path}")

    source_path.symlink_to(path)
    print(f"Created symlink: {source_path} -> {path}")

    registry = load_registry()
    registry[source_path.name] = str(source_path)
    save_registry(registry)
    print("Updated dtx.json registry.")

def apply_vault():
    if not VAULT_DIR.exists():
        print("Error: Vault is not initialized.")
        return
        
    registry = load_registry()
    if not registry:
        print("Registry is empty. Nothing to apply.")
        return

    print("Applying dotfiles from vault...")

def main():
    parser = argparse.ArgumentParser(
        prog="dtx",
        description="Minimalist dotfiles manager"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: init
    init_parser = subparsers.add_parser("init", help="Initialize the dotfiles directory")
    
    # Command: add
    add_parser = subparsers.add_parser("add", help="Add a file to the vault")
    add_parser.add_argument("file", help="Path to the file to track")

    # Command: apply
    subparsers.add_parser("apply", help="Apply tracked dotfiles to the system")

    args = parser.parse_args()

    if args.command == "init":
        init_vault()
    elif args.command == "add":
        add_file(args.file)
    elif args.command == "apply":
        apply_vault()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()