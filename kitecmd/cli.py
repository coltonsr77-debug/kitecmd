import argparse
import requests
import sys
import platform
import os
import subprocess
from importlib.metadata import version, PackageNotFoundError


def main():
    parser = argparse.ArgumentParser(
        prog="kitecmd",
        description="Kite Command Utility"
    )

    parser.add_argument(
        "--version", "-v",
        action="store_true",
        help="Show the current version of kitecmd"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # test command
    test_parser = subparsers.add_parser("test", help="Run a test message")
    test_parser.add_argument("--msg", "-m", default="This is a test.", help="Custom test message")
    test_parser.add_argument("--verbose", "-V", action="store_true", help="Show detailed system info")

    # checkupdate command
    subparsers.add_parser("checkupdate", help="Check for updates and optionally install the latest version")

    # install-IR command
    subparsers.add_parser("install-IR", help="Install the kitecmd-IR package from PyPI")

    # version command
    subparsers.add_parser("version", help="Show the current version of kitecmd")

    args = parser.parse_args()

    if args.version or args.command == "version":
        show_version("kitecmd")
    elif args.command == "test":
        run_test(args)
    elif args.command == "checkupdate":
        check_for_update("kitecmd")
    elif args.command == "install-IR":
        install_kitecmd_IR()
    else:
        parser.print_help()


def run_test(args):
    print(args.msg)
    if args.verbose:
        print("\n--- Verbose Info ---")
        print(f"kitecmd version: {get_package_version('kitecmd')}")
        print(f"Python version: {platform.python_version()}")
        print(f"Platform: {platform.system()} {platform.release()}")
        print(f"Working directory: {os.getcwd()}")
        print(f"User: {os.getenv('USERNAME') or os.getenv('USER')}")
        print("--------------------")


def get_package_version(package_name):
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "Unknown"


def show_version(package_name):
    print(f"kitecmd version {get_package_version(package_name)}")


def check_for_update(package_name):
    current_version = get_package_version(package_name)
    try:
        resp = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=5)
        resp.raise_for_status()
        latest_version = resp.json()["info"]["version"]
    except requests.RequestException as e:
        print(f"Could not fetch update info: {e}")
        sys.exit(1)

    if current_version == latest_version:
        print(f"You are using the latest version ({current_version}).")
    else:
        print("A new version is available.")
        print(f"Installed: {current_version}")
        print(f"Latest:    {latest_version}")
        answer = input("Do you want to update to the latest version? (y/n): ").strip().lower()
        if answer == "y":
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name])
                print(f"\nSuccessfully updated {package_name} to version {latest_version}.")
            except subprocess.CalledProcessError:
                print("Failed to update kitecmd. Try running as administrator or with elevated permissions.")
        else:
            print("Update cancelled.")


def install_kitecmd_IR():
    """Install the kitecmd-IR package from PyPI."""
    print("Installing kitecmd-IR...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kitecmd-IR=0.1"])
        print("\nSuccessfully installed kitecmd-IR.")
    except subprocess.CalledProcessError:
        print("Failed to install kitecmd-IR. Try running as administrator or check your internet connection.")
