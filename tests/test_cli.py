from typer.testing import CliRunner

from greynoiselabs.cli import app

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0


def test_init(mocker, tmp_path):
    # Mock the necessary methods
    mocker.patch(
        "greynoiselabs.cli.authenticate", return_value=("mock_token", "mock_user")
    )
    mocker.patch("greynoiselabs.cli.new_client", return_value="mock_client_instance")

    # Call the init command with the temporary directory
    result = runner.invoke(app, ["init", "--config", str(tmp_path)])

    assert result.exit_code == 1
    assert "You are not authenticated" in result.stdout
