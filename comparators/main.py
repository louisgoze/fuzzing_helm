import json


def compare_checkov(before_filename, after_filename) -> tuple[int, int]:
    """Returns the amount of failed tests before and after"""
    before = json.load(open(before_filename))
    after = json.load(open(after_filename))
    return before["summary"]["failed"], after["summary"]["failed"]
