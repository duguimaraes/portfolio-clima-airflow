from datetime import date
from pathlib import Path

import boto3

BUCKET_NAME = "portfolio-clima-832285994224"
SNAPSHOT_DATE = date.today().isoformat()

BRONZE_DIR = (
    Path("data/bronze/capital_forecasts")
    / f"snapshot_date={SNAPSHOT_DATE}"
)
SILVER_PATH = (
    Path("data/silver/capital_forecasts")
    / f"snapshot_date={SNAPSHOT_DATE}"
    / "weather.csv"
)
GOLD_PATH = (
    Path("data/gold/capital_forecasts")
    / f"snapshot_date={SNAPSHOT_DATE}"
    / "weather.csv"
)


def upload_file(s3_client, local_path, object_key):
    s3_client.upload_file(
        Filename=str(local_path),
        Bucket=BUCKET_NAME,
        Key=object_key,
    )
    print(f"Enviado: {local_path} -> s3://{BUCKET_NAME}/{object_key}")


def main():
    s3_client = boto3.client("s3")

    bronze_files = sorted(BRONZE_DIR.glob("*.json"))

    for bronze_path in bronze_files:
        object_key = (
            f"bronze/capital_forecasts/"
            f"snapshot_date={SNAPSHOT_DATE}/"
            f"{bronze_path.name}"
        )
        upload_file(s3_client, bronze_path, object_key)

    upload_file(
        s3_client,
        SILVER_PATH,
        f"silver/capital_forecasts/snapshot_date={SNAPSHOT_DATE}/weather.csv",
    )
    upload_file(
        s3_client,
        GOLD_PATH,
        f"gold/capital_forecasts/snapshot_date={SNAPSHOT_DATE}/weather.csv",
    )

    print(
        "Carga no S3 finalizada com sucesso. "
        f"Arquivos Bronze enviados: {len(bronze_files)}."
    )


if __name__ == "__main__":
    main()