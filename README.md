# dtx

A minimalist dotfiles manager for the command line.

`dtx` keeps your configuration files in one central vault, replaces their
original location with a symlink, and tracks everything in a simple JSON
registry — so your dotfiles stay versioned, portable, and easy to sync
across machines.

## Features

- **Vault-based tracking** — files are moved into `~/.dtx` and symlinked back
  to their original location.
- **Simple JSON registry** — `~/.dtx/dtx.json` keeps a record of every
  tracked file and where it came from.
- **Status overview** — quickly see which files are tracked, missing, or
  have a broken link.
- **No external dependencies** — built entirely on the Python standard
  library.

## Installation

`dtx` isn't published on PyPI yet, so install it directly from source:

```bash
git clone https://github.com/JeanBiza/dtx.git
cd dtx
pip install -e .
```

This installs the `dtx` command on your `PATH` using an editable install,
so any changes you pull will be reflected immediately.

**Requirements:** Python 3.8+

## Usage

### Initialize the vault

```bash
dtx init
```

Creates the vault directory at `~/.dtx`. This only needs to be run once.

### Track a file

```bash
dtx add ~/.bashrc
```

Moves `~/.bashrc` into the vault and replaces it with a symlink pointing
back to the vault copy. From then on, editing `~/.bashrc` actually edits
the file inside `~/.dtx`.

### Check status

```bash
dtx status
```

Shows every tracked file along with its state: `TRACKED`, `MISSING IN
VAULT`, or `BROKEN LINK`.

### List tracked files

```bash
dtx list
```

Prints a plain list of every file currently tracked in the registry.

### Stop tracking a file

```bash
dtx remove .bashrc
```

Removes the symlink, restores the original file from the vault back to its
original location, and removes it from the registry.

### Apply the vault to a new machine

```bash
dtx apply
```

> **Status: work in progress.** This command is scaffolded but not yet
> implemented — it's intended to recreate the symlinks for all registry
> entries on a fresh machine.

## How it works

Every tracked file lives in two places conceptually, but only one place
physically:

1. The real file is moved into the vault (`~/.dtx/<filename>`).
2. A symlink is created at the file's original path, pointing to the vault
   copy.
3. The mapping between filename and original path is saved in
   `~/.dtx/dtx.json`.

This means the vault directory itself can be version-controlled (e.g. as a
git repo) and synced across machines, while `dtx apply` (once finished)
will handle re-creating the symlinks elsewhere.

## Contributing

Contributions are very welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md)
before opening a pull request.

## License

This project is licensed under the terms of the license included in the
[LICENSE](LICENSE) file.
