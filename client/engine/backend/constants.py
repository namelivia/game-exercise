import os

env_value = os.environ.get("GRAPHICS")

if env_value is not None:
    print(f"Graphics set to: {env_value}")
    GRAPHICS = env_value
else:
    print(f"Graphics will default to native")
    GRAPHICS = "NATIVE"
