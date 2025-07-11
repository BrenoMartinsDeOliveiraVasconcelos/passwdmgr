import cli
import console

def main():
    exit_code = cli.main()

    console.clear()

    if exit_code != 0:
        exit(exit_code)

if __name__ == "__main__":
    main()