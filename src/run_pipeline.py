import subprocess
import sys


def run_step(command):
    print(f"Executando: {' '.join(command)}")
    subprocess.run(command, check=True)


def main():
    python_executable = sys.executable

    run_step([python_executable, "src/extract_weather.py"])
    run_step([python_executable, "src/transform_weather.py"])
    run_step([python_executable, "src/create_gold_weather.py"])

    print("Pipeline finalizado com sucesso.")


if __name__ == "__main__":
    main()