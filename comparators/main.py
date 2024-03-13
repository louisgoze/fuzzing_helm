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
    try:
        return len(before[0]["scoring"]["advise"]), len(after[0]["scoring"]["advise"])
    except:
        return len(before[0]["scoring"]["advise"]), 'Error'


def compare_kubeaudit(before_filename, after_filename) -> tuple[int, int]:
    """Retourne le nombre de tests échoués avant et après"""
    before, error = _execute_command_with_error(
        f"wc -l {before_filename}")
    after, error = _execute_command_with_error(
        f"wc -l {after_filename}")
    return before.strip().split(" ")[0], after.strip().split(" ")[0]


def compare_kubescore(before_filename, after_filename) -> tuple[int, int]:
    """Retourne le nombre de tests échoués avant et après"""
    before = ''.join(open(before_filename).readlines()).split('[')
    after = ''.join(open(after_filename).readlines()).split('[')
    return str(len(before)), str(len(after))
