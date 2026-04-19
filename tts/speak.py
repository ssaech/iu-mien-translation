import argparse
import json
import random
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

DEFAULT_JSON = PROJECT_ROOT / "data" / "text" / "pairs.json"
DEFAULT_MODEL = BASE_DIR / "models" / "piper" / "en_US-lessac-medium" / "en_US-lessac-medium.onnx"
DEFAULT_OUT = BASE_DIR / "out.wav"
DEFAULT_LANGUAGE = "english"

# Translated 
# fallbacks.json: fb001
# pairs.json: g007

def load_json_records(json_path: Path) -> list[dict]:
    if not json_path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_path}")

    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(f"Expected top-level JSON array in: {json_path}")

    if not data:
        raise ValueError(f"No records found in: {json_path}")

    return data


def select_record(records: list[dict], record_id: str | None) -> dict:
    if record_id is None:
        return random.choice(records)

    for record in records:
        if str(record.get("id")) == record_id:
            return record

    raise ValueError(f"No record found with id={record_id!r}")


def resolve_json_path(filepath_arg: str | None) -> Path:
    if filepath_arg is None:
        return DEFAULT_JSON

    path = Path(filepath_arg)
    if path.is_absolute():
        return path

    return (PROJECT_ROOT / path).resolve()


def get_text_from_record(record: dict, language_field: str) -> str:
    value = record.get(language_field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"Selected record has no usable '{language_field}' value: id={record.get('id')!r}"
        )
    return value.strip()


def speak_text(text: str, model_path: Path = DEFAULT_MODEL, out_path: Path = DEFAULT_OUT) -> None:
    if not model_path.exists():
        raise FileNotFoundError(f"Piper model not found: {model_path}")

    cmd = [
        "piper",
        "--model",
        str(model_path),
        "--output_file",
        str(out_path),
    ]

    subprocess.run(cmd, input=text.encode("utf-8"), check=True)
    subprocess.run(["afplay", str(out_path)], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Read a selected text field aloud using Piper.")
    parser.add_argument(
        "-f",
        "--file",
        help="Path to JSON file. Defaults to data/text/pairs.json from the project root.",
    )
    parser.add_argument(
        "-i",
        "--id",
        help="Record id to select. If omitted, a random record is used.",
    )
    parser.add_argument(
        "-l",
        "--language",
        default=DEFAULT_LANGUAGE,
        help="Field name to read from the selected record. Defaults to 'english'. Example: english, mien",
    )
    args = parser.parse_args()

    try:
        json_path = resolve_json_path(args.file)
        records = load_json_records(json_path)
        record = select_record(records, args.id)

        language_field = args.language.strip()
        if not language_field:
            raise ValueError("Language field cannot be empty.")

        text = get_text_from_record(record, language_field)

        print(f"File: {json_path}")
        print(f"Selected id: {record.get('id')}")
        print(f"Category: {record.get('category')}")
        print(f"Language field: {language_field}")
        print(f"Text: {text}")

        speak_text(text)
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())