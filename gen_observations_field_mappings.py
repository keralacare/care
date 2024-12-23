import csv
import json
import logging
from pathlib import Path

import requests

logger = logging.getLogger(__name__)


"""
This is a helper script to generate the field mapping for the daily_round to observations migration.


Fields in the CSV:

Any one of value_key or notes_key should be present

- value_key: The key to access the value in the daily_round object
- notes_key: The key to access the notes in the daily_round object

- value_type: The type of value for the observation:
    group | boolean | decimal | integer | string | text | display | date | dateTime |
    time | choice | open-choice | attachment | reference | quantity | structured

- value_map: A json mapping of values to be used for the value field, useful for mapping values to codes
eg: for rhythm
{
    0: {system: "http://loinc.org/", code: "8867-4", display_name: "Normal sinus rhythm"},
    1: {system: "http://loinc.org/", code: "271594007", display_name: "Atrial fibrillation"}
    ...
}

Below are the fields that are used to generate Coding objects:

- category_code: The code for the category of the observation, uses the HL7 observation system by default
- main_code: The main code for the observation, uses the LOINC system by default
- alternate_coding: The alternate coding for the observation, uses the SNOMED system by default
- body_site: The body site for the observation
- method: The method used for the observation
- unit_code: The code for the unit of the observation
- quantity_code: The code for the quantity of the observation

unit_code and quantity_code are only used when the value_type is quantifiable


All code fields have a corresponding display_name field which is used to
generate the display field in the Coding object, the system value is
inferred as LOINC or SNOMED if the code is a URL

"""


def make_codeable_concept(code, display_name, system=None):
    code = str(code)
    if not code:
        return {}

    # try to infer the system from the code if its a url
    if "loinc" in code:
        code = [x for x in code.split("/") if x][-1]
        system = "http://loinc.org/"
    elif "snomed" in code:
        code = [x for x in code.split("/") if x][-1]
        system = "http://www.snomed.info/sct"

    if not system:
        system = "http://example.com"

    return {
        "system": system,
        "code": code,
        "display_name": display_name,
        # TODO: add fields like version, display, userSelected, etc.
    }


def clean_csv_and_save_as_json(sheet_id):
    csv_url = (
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?gid=0&format=csv"
    )
    logger.info("Downloading CSV from %s", csv_url)

    # Download the CSV content
    response = requests.get(csv_url, timeout=10)
    response.raise_for_status()
    csv_data = response.text.splitlines()

    reader = csv.DictReader(
        csv_data,
        fieldnames=[
            "value_key",
            "notes_key",
            "category_code",
            "category_code_display_name",
            "main_code",
            "main_code_display_name",
            "alternate_coding",
            "alternate_coding_display_name",
            "value_type",
            "unit_code",
            "unit_code_display_name",
            "quantity_code",
            "quantity_code_display_name",
            "value_map",
            "body_site",
            "body_site_display_name",
            "method",
            "method_display_name",
        ],
    )

    cleaned_rows = []

    logger.info("Cleaning CSV")
    for row in reader:
        # Ensure we skip the header line if it's repeated (in case of specifying fieldnames)
        if row["value_key"] == "value_key":
            continue

        row["notes_key"] = ""

        row["value_type"] = row["value_type"].lower() or "string"

        # Convert codes to coding objects
        row["category_code"] = make_codeable_concept(
            row["category_code"],
            row["category_code_display_name"],
            "http://terminology.hl7.org/CodeSystem/observation-category",
        )

        row["main_code"] = make_codeable_concept(
            row["main_code"],
            row["main_code_display_name"],
            "http://loinc.org/",
        )

        row["alternate_coding"] = make_codeable_concept(
            row["alternate_coding"],
            row["alternate_coding_display_name"],
            "http://www.snomed.info/sct",
        )

        row["unit_code"] = make_codeable_concept(
            row["unit_code"], row["unit_code_display_name"]
        )

        row["quantity_code"] = make_codeable_concept(
            row["quantity_code"], row["quantity_code_display_name"]
        )

        row["body_site"] = make_codeable_concept(
            row["body_site"], row["body_site_display_name"]
        )

        row["method"] = make_codeable_concept(row["method"], row["method_display_name"])

        if row["value_map"]:
            row["value_map"] = json.loads(row["value_map"])

        # Remove display_name fields
        for col in [
            "category_code_display_name",
            "main_code_display_name",
            "alternate_coding_display_name",
            "unit_code_display_name",
            "quantity_code_display_name",
            "body_site_display_name",
            "method_display_name",
        ]:
            row.pop(col, None)

        cleaned_rows.append(row)

    # Convert to JSON lines
    json_file_path = (
        Path.cwd()
        / "care/emr/migrations"
        / "daily_round_to_observations_field_mapping.json"
    )
    with json_file_path.open("w", encoding="utf-8") as f:
        json.dump(cleaned_rows, f, ensure_ascii=False, indent=2)

    logger.info("Cleaned data saved to %s", json_file_path)


# https://docs.google.com/spreadsheets/d/1xgR5G1NFAKo0mODKUULOZapCtuaP-wd5kEacky0RNJA/edit
sheet_id = "1xgR5G1NFAKo0mODKUULOZapCtuaP-wd5kEacky0RNJA"
clean_csv_and_save_as_json(sheet_id)
