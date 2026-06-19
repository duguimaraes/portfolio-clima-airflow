from pathlib import Path

import boto3

BUCKET_NAME = "portfolio-clima-832285994224"

FILES_TO_UPLOAD = [
    (Path("data/bronze/weather_cuiaba.json"), "bronze/weather_cuiaba.json"),
    (Path("data/silver/weather_cuiaba.csv"), "silver/weather_cuiaba.csv"),
    (Path("data/gold/weather_cuiaba_summary.csv"), "gold/weather_cuiaba_summary.csv"),
]

def upload_file(s3_client, local_path, object_key):
    s3_client.upload_file(
        Filename=str(local_path),
        Bucket=BUCKET_NAME,
        Key=object_key,
    )
    print(f"Enviado: {local_path} -> s3://{BUCKET_NAME}/{object_key}")

def main():
    s3_client = boto3.client("s3")

    for local_path, object_key in FILES_TO_UPLOAD:
        upload_file(s3_client, local_path, object_key)

    print("Carga no S3 finalizada com sucesso.")


if __name__ == "__main__":
    main()