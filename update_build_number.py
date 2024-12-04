import re
import sys
from pathlib import Path

from loguru import logger

# Path to your __init__.py file
INIT_FILE_PATH = Path("homebin/__init__.py")


def update_build_number():
    if not INIT_FILE_PATH.exists():
        logger.error(f"Error: {INIT_FILE_PATH} does not exist.")
        return 1

    content = INIT_FILE_PATH.read_text()

    # Search for the build number field
    match = re.search(r"__build__\s*=\s*(\d+)", content)
    if match:
        current_build = int(match.group(1))
        new_build = current_build + 1
        content = re.sub(r"(__build__\s*=\s*)\d+", f"\\1{new_build}", content)
    else:
        # If the field doesn't exist, append it
        new_build = 1
        content += f"\n__build__ = {new_build}\n"

    # Write the updated content back
    INIT_FILE_PATH.write_text(content)
    logger.success(f"Updated build number to {new_build} in {INIT_FILE_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(update_build_number())
