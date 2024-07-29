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


def _store_file(file: str, output: str) -> None:
    iac = open(file, "w")
    iac.write(output)
    iac.close()


def run_checkov(directory: str, output_file: str):
    log.info("Running checkov")
    output, error = _execute_command_with_error(
        f"checkov --file {directory} --framework kubernetes --output json")
    if error is not None and len(error) > 1:
        log.error("Could not run checkov", error)
        os._exit(1)
    _store_file(output_file, output)


def run_kubesec(directory: str, output_file: str):
    log.info("Running kubesec")
    output, error = _execute_command_with_error(
        f"kubesec scan {directory}")
    _store_file(output_file, output)


def run_kubeaudit(directory: str, output_file: str):
    log.info("Running kubeaudit")
    output, error = _execute_command_with_error(
        f"kubeaudit all -f {directory} --format=json")
    _store_file(output_file, output)


def run_kubescore(directory: str, output_file: str):
    log.info("Running kubescore")
    output, error = _execute_command_with_error(
        f"kube-score score {directory}")
    _store_file(output_file, output)
