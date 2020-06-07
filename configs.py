import anyconfig

configs = ["config.yml", "config.local.yml"]
conf = anyconfig.load(configs, ac_parser="yaml")
