import csv
from dataclasses import dataclass, fields, asdict
from typing import List
import yaml
import rules
import runners
import comparators
from benedict import benedict
import argparse
import subprocess


@dataclass
class FuzzResult:
    Misconfiguration: str
    Tool: str
    N_misc_before: str
    N_misc_after: str
    Undetected: str
    Is_applied: bool


def _execute_command_with_error(command: str):
    output, error = subprocess.Popen(command.split(
        " "), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if error is not None:
        return output.decode("utf-8"), error.decode("utf-8")
    return output.decode("utf-8"), None


def to_stdout(final_dict):
    print(yaml.safe_dump(final_dict))


def save_yaml(final_dict, filerule_name):
    with open(filerule_name, 'w') as outfile:
        outfile.write(final_dict.to_yaml())


def read_yaml(filerule_name) -> dict:
    input_file = open(filerule_name, "r")
    yaml_data = benedict(yaml.safe_load(input_file))
    return yaml_data


if __name__ == "__main__":
    results: List[FuzzResult] = []
    parser = argparse.ArgumentParser(description='Yaml fuzzer')
    parser.add_argument(
        '-f', '--file', help='Input YAML file to fuzz', type=str, required=True)
    args = parser.parse_args()

    input_data = read_yaml(args.file)

    for rule_name, rule_fn in rules.__dict__.items():  # For each fuzz rule
        if callable(rule_fn):
            output_rule_name = "output/output_" + rule_name + ".yml"
            print("Running fuzzer:", rule_name)
            for runner, runner_fn in runners.__dict__.items():  # For each security checker
                if callable(runner_fn):
                    # 1 - Run the security checker on input
                    runner_fn(
                        args.file, f"scan_results/{runner.split('_')[1]}_before_{rule_name}.json")

                    # 2 - Apply fuzz rule
                    fuzzed_input = rule_fn(input_data)
                    assert fuzzed_input != input_data
                    # 3 - Store fuzz rule
                    save_yaml(fuzzed_input, output_rule_name)
                    # 4 - Run the security checker on fuzzed input
                    runner_fn(
                        output_rule_name, f"scan_results/{runner.split('_')[1]}_after_{rule_name}.json")
        else:
            continue
        for comparator_name, comparator_fn in comparators.__dict__.items():
            if callable(comparator_fn):
                before, after = comparator_fn(
                    f"scan_results/{comparator_name.split('_')[1]}_before_{rule_name}.json", f"scan_results/{comparator_name.split('_')[1]}_after_{rule_name}.json")
                out, err = _execute_command_with_error(
                    f"kubectl apply -f output/output_{rule_name}.yml")
                undetected = False
                try:
                    bint = int(before)
                    aint = int(after)
                    if aint > bint:
                        undetected = False
                    else:
                        undetected = True
                except:
                    undetected = False
                finally:
                    _execute_command_with_error(
                    f"kubectl delete -f output/output_{rule_name}.yml")
                results.append(FuzzResult(rule_name,
                                          comparator_name.split('_')[1], before, after, undetected, True if len(err) == 0 else False))
                if len(err):
                    print(err)
    with open('fuzz_result.csv', 'w') as f:
        flds = [fld.name for fld in fields(FuzzResult)]
        w = csv.DictWriter(f, flds)
        w.writeheader()
        w.writerows([asdict(prop) for prop in results])
