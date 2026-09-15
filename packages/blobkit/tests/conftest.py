import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "accelerator: requires optional JAX")
    config.addinivalue_line("markers", "slow: longer numerical and assay regression checks")


def pytest_addoption(parser):
    parser.addoption("--require-gpu", action="store_true", help="fail if JAX has no GPU")


def pytest_sessionstart(session):
    if session.config.getoption("--require-gpu"):
        import jax

        if not any(device.platform == "gpu" for device in jax.devices()):
            raise pytest.UsageError("--require-gpu requested, but JAX has no GPU device")


@pytest.fixture(scope="session")
def accelerator():
    jax = pytest.importorskip("jax")
    jax.config.update("jax_enable_x64", True)
    return jax
