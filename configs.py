import os

import anyconfig

is_prod = os.getenv("PRODUCTION_SERVER")
conf = anyconfig.load("config.local.yml" if is_prod else "config.yml")
