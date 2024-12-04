import logging
import re
import sys
from datetime import datetime
from pathlib import Path

import pytz

logger = logging.getLogger(__name__)

# Path to your __init__.py file
INIT_FILE_PATH = Path("homebin/__init__.py")


def generate_build_number(time_zone: str = "UTC") -> str:
    """Generate a build number based on the current date and time.

    The first 8 characters of the build number are the current date in the format
    'YYYYMMDD'. The last 3 characters ara counter of 2 minute intervals since midnight.

    Examples:
        >>> generate_build_number()
        '20220131120'

    Args:
        time_zone (str, optional): The time zone to use for the build number. Defaults to 'UTC'.

    Returns:
        str: The generated build number"""  # noqa: E501
    timezone_obj = pytz.timezone(time_zone)
    now = datetime.now(timezone_obj)
    build_number = now.strftime("%Y%m%d")
    build_number += str((now.hour * 60 + now.minute) // 2).zfill(3)
    return build_number


def update_build_number():
    if not INIT_FILE_PATH.exists():
        logger.error("Error: %s does not exist.", INIT_FILE_PATH)
        return 1

    content = INIT_FILE_PATH.read_text()

    new_build = generate_build_number()
    # Search for the build number field
    match = re.search(r"__build__\s*=\s*\"(\d+)\"", content)
    if match:
        content = re.sub(r"(__build__\s*=\s*)\"\d+\"", f'\\g<1>"{new_build}"', content)
    else:
        # If the field doesn't exist, append it
        content += f"\n__build__ = {new_build}\n"

    # Write the updated content back
    INIT_FILE_PATH.write_text(content)
    logger.info("Updated build number to %s in %s", new_build, INIT_FILE_PATH)
    return 0


if __name__ == "__main__":
    sys.exit(update_build_number())
