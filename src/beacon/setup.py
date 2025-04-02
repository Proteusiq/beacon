"""Legacy setup module - use beacon-db CLI instead."""
from beacon.cli.db import init

if __name__ == "__main__":
    print("WARNING: This script is deprecated. Use 'beacon-db init' instead.")
    init()
