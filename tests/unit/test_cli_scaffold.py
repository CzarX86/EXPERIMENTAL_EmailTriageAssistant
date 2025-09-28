import os
import subprocess
import sys


def test_cli_hello_runs(tmp_path):
    # Run the CLI entrypoint using Python
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    cli_path = os.path.join(repo_root, "src", "cli", "main.py")
    assert os.path.exists(cli_path)
    env = os.environ.copy()
    # Ensure the local 'src' package is importable when running as a file
    env["PYTHONPATH"] = repo_root + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, cli_path, "hello", "Alice"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert proc.returncode == 0
    assert "Hello, Alice" in proc.stdout
