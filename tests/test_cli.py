import json

import dtx.cli as cli


# --- registry helpers -------------------------------------------------

def test_load_registry_returns_empty_dict_when_missing(vault):
    assert cli.load_registry() == {}


def test_save_and_load_registry_roundtrip(initialized_vault):
    data = {"file.txt": "/home/user/file.txt"}
    cli.save_registry(data)

    assert cli.REGISTRY_FILE.exists()
    assert cli.load_registry() == data


# --- init ---------------------------------------------------------------

def test_init_vault_creates_directory(vault, capsys):
    assert not vault.exists()

    cli.init_vault()

    assert vault.exists()
    out = capsys.readouterr().out
    assert "Initialized empty vault" in out


def test_init_vault_does_not_fail_if_already_exists(initialized_vault, capsys):
    cli.init_vault()

    out = capsys.readouterr().out
    assert "already exists" in out


# --- add ------------------------------------------------------------------

def test_add_file_moves_file_and_creates_symlink(initialized_vault, tmp_path, capsys):
    source = tmp_path / "myconf"
    source.write_text("hello")

    cli.add_file(str(source))

    vault_copy = initialized_vault / "myconf"
    assert vault_copy.exists()
    assert vault_copy.read_text() == "hello"

    assert source.is_symlink()
    assert source.resolve() == vault_copy.resolve()

    registry = cli.load_registry()
    assert registry["myconf"] == str(source)


def test_add_file_fails_if_vault_not_initialized(vault, tmp_path, capsys):
    source = tmp_path / "myconf"
    source.write_text("hello")

    cli.add_file(str(source))

    assert source.exists() and not source.is_symlink()
    out = capsys.readouterr().out
    assert "not initialized" in out


def test_add_file_fails_if_source_missing(initialized_vault, tmp_path, capsys):
    missing = tmp_path / "does_not_exist"

    cli.add_file(str(missing))

    out = capsys.readouterr().out
    assert "does not exist" in out


def test_add_file_fails_if_already_tracked(initialized_vault, tmp_path, capsys):
    source = tmp_path / "myconf"
    source.write_text("hello")
    cli.add_file(str(source))

    other_source = tmp_path / "other_dir" / "myconf"
    other_source.parent.mkdir()
    other_source.write_text("world")

    cli.add_file(str(other_source))

    out = capsys.readouterr().out
    assert "already tracked" in out


# --- remove -----------------------------------------------------------

def test_remove_file_restores_original_location(initialized_vault, tmp_path):
    source = tmp_path / "myconf"
    source.write_text("hello")
    cli.add_file(str(source))

    cli.remove_file("myconf")

    assert source.exists()
    assert not source.is_symlink()
    assert source.read_text() == "hello"
    assert cli.load_registry() == {}


def test_remove_file_fails_if_not_tracked(initialized_vault, capsys):
    cli.remove_file("nope.txt")

    out = capsys.readouterr().out
    assert "not tracked" in out


def test_remove_file_fails_if_vault_not_initialized(vault, capsys):
    cli.remove_file("nope.txt")

    out = capsys.readouterr().out
    assert "not initialized" in out


# --- status / list -----------------------------------------------------

def test_show_status_reports_no_vault(vault, capsys):
    cli.show_status()

    out = capsys.readouterr().out
    assert "not initialized" in out


def test_show_status_reports_empty_vault(initialized_vault, capsys):
    cli.show_status()

    out = capsys.readouterr().out
    assert "vault is empty" in out


def test_show_status_reports_tracked_file(initialized_vault, tmp_path, capsys):
    source = tmp_path / "myconf"
    source.write_text("hello")
    cli.add_file(str(source))
    capsys.readouterr() 

    cli.show_status()

    out = capsys.readouterr().out
    assert "myconf" in out
    assert "TRACKED" in out


def test_show_list_prints_tracked_filenames(initialized_vault, tmp_path, capsys):
    source = tmp_path / "myconf"
    source.write_text("hello")
    cli.add_file(str(source))
    capsys.readouterr()

    cli.show_list()

    out = capsys.readouterr().out
    assert "myconf" in out