# Contributing to dtx

Thanks for considering a contribution! `dtx` is a small project and every
bit of help — bug reports, documentation fixes, or new features — is
appreciated.

## Getting started

1. Fork the repository and clone your fork:

   ```bash
   git clone https://github.com/<your-username>/dtx.git
   cd dtx
   ```

2. Create a virtual environment and install the project in editable mode,
   including the dev dependencies (pytest):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

3. Confirm the CLI works:

   ```bash
   dtx --help
   ```

4. Confirm the test suite passes:

   ```bash
   pytest -v
   ```

## Making changes

- Create a new branch off `master` for your work:

  ```bash
  git checkout -b feat/short-description
  ```

- Keep pull requests focused on a single change. Smaller PRs are easier to
  review and merge.
- Follow the existing code style: standard library only, simple functions,
  no unnecessary abstractions. If you want to introduce a new dependency,
  open an issue first to discuss it.
- Add or update docstrings/comments where the intent of the code isn't
  obvious.

## Commit messages

This project loosely follows [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add support for tracking directories
fix: handle missing vault directory in remove command
docs: update README usage examples
```

Common prefixes: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.

## Testing

`dtx` has a pytest suite under `tests/`. Every test runs against an isolated,
temporary vault (see `tests/conftest.py`), so running them never touches your
real `~/.dtx`.

```bash
pip install -e ".[dev]"   # if you haven't already
pytest -v
```

If you add a new feature or fix a bug, please add a test for it. A PR
without tests for new behavior will likely get a request to add some before
it's merged.

Every push to `master` and every pull request automatically runs the test
suite via GitHub Actions across Python 3.9–3.12 (see
`.github/workflows/tests.yml`). The PR will show a green check once it
passes — no need to run anything manually beyond your local `pytest`.

## Submitting a pull request

1. Push your branch to your fork.
2. Open a pull request against `master` on `JeanBiza/dtx`.
3. Describe what the change does and why. Make sure `pytest` passes locally
   — CI will run it again automatically, but catching failures early saves
   a round trip.
4. Be ready for a round of feedback — discussion is part of the process,
   not a sign something is wrong with your contribution.

## Reporting bugs / suggesting features

Open an issue with:

- A clear, descriptive title.
- Steps to reproduce (for bugs) or the motivation/use case (for features).
- Your OS and Python version.
