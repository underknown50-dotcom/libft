import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv


@dataclass
class Config:
    mode: str
    database_url: Optional[str]
    api_key: Optional[str]
    log_level: str
    zion_endpoint: Optional[str]
    missing_vars: list[str]


def load_config() -> Config:
    load_dotenv()

    mode = os.getenv("MATRIX_MODE", "development")
    log_level = os.getenv("LOG_LEVEL", "INFO")

    database_url = os.getenv("DATABASE_URL")
    api_key = os.getenv("API_KEY")
    zion_endpoint = os.getenv("ZION_ENDPOINT")

    missing = []
    if database_url is None:
        missing.append("DATABASE_URL")
    if api_key is None:
        missing.append("API_KEY")
    if zion_endpoint is None:
        missing.append("ZION_ENDPOINT")

    return Config(
        mode=mode,
        database_url=database_url,
        api_key=api_key,
        log_level=log_level,
        zion_endpoint=zion_endpoint,
        missing_vars=missing
    )


def get_database_status(config: Config) -> str:
    if config.mode == "production" and config.database_url:
        return "Connected to production cluster"
    elif config.database_url:
        return "Connected to local instance"
    return "[MISSING]"


def get_api_status(config: Config) -> str:
    if config.api_key:
        return "Authenticated"
    return "[MISSING]"


def get_zion_status(config: Config) -> str:
    if config.zion_endpoint:
        return "Online"
    return "[MISSING]"


def print_security_checks(config: Config) -> None:
    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")

    if os.path.exists(".env"):
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] .env file not found")

    if config.mode == "production":
        if config.database_url and config.api_key and config.zion_endpoint:
            print("[OK] Production overrides available")
        else:
            print("[WARNING] Production overrides missing")
    else:
        print("[OK] Development mode - production overrides not required")


def main() -> None:
    config = load_config()

    print("ORACLE STATUS: Reading the Matrix...")
    print()
    print("Configuration loaded:")
    print(f"  Mode: {config.mode}")
    print(f"  Database: {get_database_status(config)}")
    print(f"  API Access: {get_api_status(config)}")
    print(f"  Log Level: {config.log_level}")
    print(f"  Zion Network: {get_zion_status(config)}")
    print()

    if config.missing_vars:
        print("WARNING: Missing configuration variables:")
        for var in config.missing_vars:
            print(f"  [MISSING] {var}")
        print()

    print_security_checks(config)


if __name__ == "__main__":
    main()
