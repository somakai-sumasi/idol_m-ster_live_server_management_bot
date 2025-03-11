import sys
import os
import runpy


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_script.py <script_name.py>")
        sys.exit(1)

    script_name = sys.argv[1]

    # 実行するスクリプトのフルパス
    script_path = os.path.join(os.path.dirname(__file__), "modifications", script_name)

    if not os.path.isfile(script_path):
        print(f"Error: Script '{script_name}' not found in modifications/")
        sys.exit(1)

    # スクリプトを実行
    runpy.run_path(script_path, run_name="__main__")


if __name__ == "__main__":
    main()
