import subprocess


def get_git_commit_hash():
    try:
        return (
            subprocess.check_output(  # noqa: S603
                ["git", "rev-parse", "--short", "HEAD"]  # noqa: S607
            )
            .strip()
            .decode("utf-8")
        )
    except subprocess.CalledProcessError:
        return None
