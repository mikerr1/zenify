import sys
import os
from pathlib import Path

# Scraper settings
domain_name = "zoro.com"

# Cache lifetime in seconds.
# Scraped data will be cached and have n (seconds) lifetime
# Set to 3600 for hourly cache
cache_lifetime = 10

cache_directory_name = "cache"

# Program settings
#
# DO NOT MODIFY BELOW THIS LINE
global_timeout = 5
headers_file = "headers.py"
settings_file = "settings.py"
enable_logging = True


# Resolve path
def resolve_path():
    project_root = Path(os.getcwd()).parent
    sys.path.append(str(project_root)) if project_root not in sys.path else ...


resolve_path()
# print(sys.path)