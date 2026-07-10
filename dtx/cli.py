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

def show_list():
    if not VAULT_DIR.exists():
        print("Error: Vault is not initialized.")
        return

    registry = load_registry()
    
    if not registry:
        print("No files are currently being tracked. The vault is empty.")
        print("Use 'dtx add <file>' to start tracking.")
        return

    print("List of all tracked dotfiles:\n")

    for filename in registry:
        print(f"- {filename}")
    print()

def add_file(filepath):
    source_path = Path(filepath).resolve()

    if not source_path.exists() or not source_path.is_file():
        print(f"Error: '{source_path}' does not exist or is not a regular file.")
        return

    if not VAULT_DIR.exists():
        print("Error: Vault is not initialized. Run 'dtx init' first.")
        return

    relative = source_path.relative_to("/")
    vault_path = VAULT_DIR / relative

    if vault_path.exists():
        print(f"Error: '{source_path.name}' is already tracked in the vault.")
        return

    vault_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source_path), str(vault_path))
    print(f"Moved to vault: {vault_path}")

    source_path.symlink_to(vault_path)
    print(f"Created symlink: {source_path} -> {vault_path}")

    registry = load_registry()
    registry[str(relative)] = str(source_path)
    save_registry(registry)
    print("Updated dtx registry.")

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
        original_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(vault_file), str(original_path))
        print(f"Restored file to original location: {original_path}")
    else:
        print(f"Warning: File '{filename}' was missing from the vault. It might have been deleted manually.")

    del registry[filename]
    save_registry(registry)
    print(f"Stopped tracking '{filename}'. Updated dtx.json registry.")

def untrack_file(filename):
    if not VAULT_DIR.exists():
        print("Error: Vault is not initialized.")
        return

    registry = load_registry()

    if filename not in registry:
        print(f"Error: '{filename}' is not tracked in the vault.")
        return

    del registry[filename]
    save_registry(registry)
    print(f"Stopped tracking '{filename}' (file left in vault, symlink kept).")
 
def apply_vault():
    if not VAULT_DIR.exists():
        print("Error: Vault is not initialized.")
        return
        
    registry = load_registry()
    if not registry:
        print("Registry is empty. Nothing to apply.")
        return
 
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
 
    print("Applying dotfiles from vault...\n")
 
    linked = 0
    up_to_date = 0
    skipped = 0
 
    for filename, original_path_str in registry.items():
        vault_path = VAULT_DIR / filename
        original_path = Path(original_path_str)
 
        if not vault_path.exists():
            print(f"  {RED}[SKIP]{RESET} '{filename}': missing from vault, can't apply.")
            skipped += 1
            continue
 
        if original_path.is_symlink():
            if original_path.resolve() == vault_path.resolve():
                print(f"  {GREEN}[OK]{RESET} '{filename}': already linked correctly.")
                up_to_date += 1
                continue
            original_path.unlink()
            print(f"  {YELLOW}[FIX]{RESET} '{filename}': replaced a stale symlink.")
        elif original_path.exists():
            print(f"  {RED}[SKIP]{RESET} '{filename}': a real file already exists at "
                  f"'{original_path}'. Remove or back it up, then run 'dtx apply' again.")
            skipped += 1
            continue
 
        original_path.parent.mkdir(parents=True, exist_ok=True)
        original_path.symlink_to(vault_path)
        print(f"  {GREEN}[LINKED]{RESET} '{filename}' -> {original_path}")
        linked += 1
 
    print(f"\nDone. {linked} linked, {up_to_date} already up to date, {skipped} skipped.")
 

def main():
    parser = argparse.ArgumentParser(
        prog="dtx",
        description="Minimalist dotfiles manager"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: init
    subparsers.add_parser("init", help="Initialize the dotfiles directory")

    # Command: status
    subparsers.add_parser("status", help="Show the status of all tracked dotfiles")

    # Command: list
    subparsers.add_parser("list", help="Show all tracked dotfiles")
    
    # Command: add
    add_parser = subparsers.add_parser("add", help="Add a file to the vault")
    add_parser.add_argument("file", help="Path to the file to track")

    # Command: remove
    remove_parser = subparsers.add_parser("remove", help="Stop tracking a file and restore it to its original location")
    remove_parser.add_argument("file", help="Name of the file to stop tracking (e.g., test.txt)")

    # Command: untrack
    untrack_parser = subparsers.add_parser("untrack", help="Remove a file from the registry without restoring it")
    untrack_parser.add_argument("file", help="Name of the file to untrack")

    # Command: apply
    subparsers.add_parser("apply", help="Apply tracked dotfiles to the system")

    args = parser.parse_args()

    if args.command == "init":
        init_vault()
    elif args.command == "status":
        show_status()
    elif args.command == "list":
        show_list()
    elif args.command == "add":
        add_file(args.file)
    elif args.command == "apply":
        apply_vault()
    elif args.command == "remove":
        arg = args.file
        registry = load_registry()

        if arg in registry:
            remove_file(arg)
        else:
            source_path = Path(arg).expanduser().resolve()
            relative = str(source_path.relative_to("/"))
            if relative in registry:
                remove_file(relative)
            else:
                matches = [k for k in registry if Path(k).name == arg]
                if len(matches) == 1:
                    remove_file(matches[0])
                elif len(matches) > 1:
                    print(f"Ambiguous: '{arg}' matches multiple tracked files:")
                    for m in matches:
                        print(f"  {m}")
                    print("Use the full path to specify which one.")
                else:
                    print(f"Error: '{arg}' is not tracked in the vault")
    elif args.command == "untrack":
        arg = args.file
        registry = load_registry()

        if arg in registry:
            untrack_file(arg)
        else:
            source_path = Path(arg).expanduser().resolve()
            relative = str(source_path.relative_to("/"))
            if relative in registry:
                untrack_file(relative)
            else:
                matches = [k for k in registry if Path(k).name == arg]
                if len(matches) == 1:
                    untrack_file(matches[0])
                elif len(matches) > 1:
                    print(f"Ambiguous: '{arg}' matches multiple tracked files:")
                    for m in matches:
                        print(f"  {m}")
                    print("Use the full path to specify which one.")
                else:
                    print(f"Error: '{arg}' is not tracked in the vault")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()