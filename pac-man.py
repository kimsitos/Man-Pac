from src.scheduler import GameScheduler
import sys

if __name__ == "__main__":
    try:
        GameScheduler().run()
    except FileNotFoundError as e:
        print("\033[91mFile not found Error:\033[0m", e)
        sys.exit(1)
