__version__ = "0.2.0a14"
__version_info__ = tuple(
    int(num) if num.isdigit() else num
    for num in __version__.replace("-", ".", 1).split(".")
)
__build__ = "20250205300"
