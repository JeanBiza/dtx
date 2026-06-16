import pytest
 
import dtx.cli as cli
 
 
@pytest.fixture
def vault(tmp_path, monkeypatch):
    """
    Redirects dtx's vault and registry file to a temporary directory so
    tests never touch the real ~/.dtx on the machine running them.
    """
    vault_dir = tmp_path / ".dtx"
    registry_file = vault_dir / "dtx.json"
 
    monkeypatch.setattr(cli, "VAULT_DIR", vault_dir)
    monkeypatch.setattr(cli, "REGISTRY_FILE", registry_file)
 
    return vault_dir
 
 
@pytest.fixture
def initialized_vault(vault):
    """Same as `vault`, but already initialized (mkdir already ran)."""
    vault.mkdir(parents=True)
    return vault
 