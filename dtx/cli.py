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

def show_status():
    if not VAULT_DIR.exists():
        print("Error: Vault is not initialized.")
        return

    registry = load_registry()
    
    if not registry:
        print("No files are currently being tracked. The vault is empty.")
        print("Use 'dtx add <file>' to start tracking.")
        return

    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

    print("Currently tracked dotfiles:\n")

    for filename, original_path_str in registry.items():
        original_path = Path(original_path_str)
        vault_path = VAULT_DIR / filename
        
        if not vault_path.exists():
            status_tag = f"{RED}[MISSING IN VAULT]{RESET}"
        elif not original_path.is_symlink():
            status_tag = f"{RED}[BROKEN LINK]{RESET}"
        else:
            status_tag = f"{GREEN}[TRACKED]{RESET}"

        print(f"  {status_tag} {filename}")
        print(f"      Target: {original_path}")
    
    print("\nSystem check complete.")

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

def remove_file(filename):
    if not VAULT_DIR.exists():
        print("Error: Vault is not initialized.")
        return

    registry = load_registry()
    
    if filename not in registry:
        print(f"Error: '{filename}' is not tracked in the vault.")
        return

    original_path_str = registry[filename]
    original_path = Path(original_path_str)
    vault_file = VAULT_DIR / filename

    if original_path.is_symlink():
        original_path.unlink()
        print(f"Removed symlink: {original_path}")
    elif original_path.exists():
        print(f"Warning: '{original_path}' exists but is not a symlink. Skipping symlink deletion.")

    if vault_file.exists():
        shutil.move(str(vault_file), str(original_path))
        print(f"Restored file to original location: {original_path}")
    else:
        print(f"Warning: File '{filename}' was missing from the vault. It might have been deleted manually.")

    del registry[filename]
    save_registry(registry)
    print(f"Stopped tracking '{filename}'. Updated dtx.json registry.")

def apply_vault():
    if not VAULT_DIR.exists():
        print("Error: Vault is not initialized.")
        return
        
    registry = load_registry()
    if not registry:
        print("Registry is empty. Nothing to apply.")
        return

    print("Applying dotfiles from vault...")
    
    #TODO apply

def main():
    parser = argparse.ArgumentParser(
        prog="dtx",
        description="Minimalist dotfiles manager"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: init
    init_parser = subparsers.add_parser("init", help="Initialize the dotfiles directory")

    # Command: status
    subparsers.add_parser("status", help="Show the status of all tracked dotfiles")
    
    # Command: add
    add_parser = subparsers.add_parser("add", help="Add a file to the vault")
    add_parser.add_argument("file", help="Path to the file to track")

    # Command: remove
    remove_parser = subparsers.add_parser("remove", help="Stop tracking a file and restore it to its original location")
    remove_parser.add_argument("file", help="Name of the file to stop tracking (e.g., test.txt)")

    # Command: apply
    subparsers.add_parser("apply", help="Apply tracked dotfiles to the system")

    args = parser.parse_args()

    if args.command == "init":
        init_vault()
    elif args.command == "status":
        show_status()
    elif args.command == "add":
        add_file(args.file)
    elif args.command == "apply":
        apply_vault()
    elif args.command == "remove":
        filename = Path(args.file).name
        remove_file(filename)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()