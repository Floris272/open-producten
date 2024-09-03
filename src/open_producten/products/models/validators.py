import json
import re
from datetime import datetime
from json.decoder import JSONDecodeError

from django.core.exceptions import ValidationError

from open_producten.producttypes.models import FieldTypes


def validate_bsn(bsn: str):
    """
    Validates that a bsn number is 9 digits and runs the 11 check.
    """

    if not re.match(r"^[0-9]{9}$", bsn):
        raise ValidationError("A bsn number consists of 9 digits.")

    total = sum(int(num) * (9 - i) for i, num in enumerate(bsn[:8]))
    total += int(bsn[8]) * -1

    if total == 0 or total % 11 != 0:
        raise ValidationError("Invalid bsn number")


def validate_checkbox(value: str):
    if value != "true" and value != "false":
        raise ValidationError("Checkbox must be true or false")


def validate_datetime_format(value: str, _format: str, field_type: FieldTypes):
    try:
        datetime.strptime(value, _format)
    except ValueError:
        raise ValidationError(f"{field_type} should use {_format} format")


def validate_regex(value: str, pattern: str, field_type: FieldTypes):
    if not re.match(pattern, value):
        raise ValidationError(f"invalid {field_type}")


def _load_json(value: str):
    try:
        value = json.loads(value)
    except JSONDecodeError:
        raise ValidationError("invalid json")
    return value


def validate_select_boxes(value: str, choices: list[str]):
    value = _load_json(value)
    for v in set(value.values()):
        if not isinstance(v, bool):
            raise ValidationError("select box values should be boolean")

    if unknown_keys := set(value.keys()) - set(choices):
        raise ValidationError(
            f"keys {', '.join(unknown_keys)} are not in the field choices"
        )

    if missing_keys := set(choices) - set(value.keys()):
        raise ValidationError(f"keys {', '.join(missing_keys)} are missing in data")


def choice_exists(value: str, choices: list[str]):
    if value not in choices:
        raise ValidationError("value does not exist in the field choices")


def validate_radio(value: str, choices: list[str]):
    choice_exists(value, choices)


def validate_select(value: str, choices: list[str]):
    validate_regex(value, "^(.*,?)+$", FieldTypes.SELECT)

    for d in value.split(","):
        choice_exists(d, choices)
