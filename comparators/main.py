import json
import os
import logging
import subprocess
log: logging.Logger = logging.getLogger('custom_logger')


def _execute_command_with_error(command: str):
    output, error = subprocess.Popen(command.split(
        " "), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if error is not None:
        return output.decode("utf-8"), error.decode("utf-8")
    return output.decode("utf-8"), None


def compare_checkov(before_filename, after_filename) -> tuple[int, int]:
    """Returns the amount of failed tests before and after"""
    before = json.load(open(before_filename))
    after = json.load(open(after_filename))
    return before["summary"]["failed"], after["summary"]["failed"]


def compare_kubesec(before_filename, after_filename) -> tuple[int, int]:
    """Retourne le nombre de tests échoués avant et après"""
    before = json.load(open(before_filename))
    after = json.load(open(after_filename))
    return len(before[0]["scoring"]["advise"]), len(after[0]["scoring"]["advise"])


def compare_kubeaudit(before_filename, after_filename) -> tuple[int, int]:
    """Retourne le nombre de tests échoués avant et après"""
    before, error = _execute_command_with_error(
        f"wc -l {before_filename}")
    after, error = _execute_command_with_error(
        f"wc -l {after_filename}")
    return before.split(" ")[0], after.split(" ")[0]


def compare_kubescore(before_filename, after_filename) -> tuple[int, int]:
    """Retourne le nombre de tests échoués avant et après"""
    before, error = _execute_command_with_error(
        f"grep -c '\[' {before_filename}")
    after, error = _execute_command_with_error(
        f"grep -c '\[' {after_filename}")
    return before[0], after[0]
