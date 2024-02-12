import os
import logging
import subprocess
log: logging.Logger = logging.getLogger('custom_logger')


def execute_command_with_error(command: str):
    output, error = subprocess.Popen(command.split(
        " "), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if error is not None:
        if len(error) > 1:
            log.warn(error.decode("utf-8"))
        return output.decode("utf-8"), error.decode("utf-8")
    return output.decode("utf-8"), None


def store_file(file: str, output: str) -> None:
    iac = open(file, "w")
    iac.write(output)
    iac.close()

def run_checkov(directory: str, output_file: str):
    log.info("Running checkov")
    output, error = execute_command_with_error(
        f"checkov -d {directory} --framework kubernetes --output json")
    if error is not None and len(error) > 1:
        log.error("Could not run checkov", error)
        os._exit(1)
    store_file(output_file, output)
