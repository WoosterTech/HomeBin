import subprocess


def get_git_commit_hash():
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])  # noqa: S603, S607
            .strip()
            .decode("utf-8")
        )
    except subprocess.CalledProcessError:
        return None
