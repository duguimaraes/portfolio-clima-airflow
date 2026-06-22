import subprocess
import sys


def run_step(command):
    print(f"Executando: {' '.join(command)}")
    subprocess.run(command, check=True)


def main():
    python_executable = sys.executable

    run_step([python_executable, "src/extract_capitals_weather.py"])
    run_step([python_executable, "src/transform_capitals_weather.py"])
    run_step([python_executable, "src/create_capitals_gold.py"])
    run_step([python_executable, "src/load_capitals_to_s3.py"])

    print("Pipeline de capitais finalizada com sucesso.")


if __name__ == "__main__":
    main()