import yaml
import rules
import runners
import comparators
from benedict import benedict
import argparse
import os


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
    parser = argparse.ArgumentParser(description='Yaml fuzzer')
    parser.add_argument(
        '-f', '--file', help='Input YAML file to fuzz', type=str, required=True)
    args = parser.parse_args()

    input_data = read_yaml(args.file)

    for rule_name, fn in rules.__dict__.items():  # For each fuzz rule
        if callable(fn):
            output_rule_name = "output/output_" + rule_name + ".yml"
            print("Running fuzzer:", rule_name)
            for runner, runner_fn in runners.__dict__.items():  # For each security checker
                if callable(runner_fn):
                    # 1 - Run the security checker on input
                    runner_fn(
                        args.file, f"scan_results/{runner.split('_')[1]}_before_{rule_name}.json")

                    # 2 - Apply fuzz rule
                    fuzzed_input = fn(input_data)
                    assert fuzzed_input != input_data
                    # 3 - Store fuzz rule
                    save_yaml(fuzzed_input, output_rule_name)
                    # 4 - Run the security checker on fuzzed input
                    runner_fn(
                        args.file, f"scan_results/{runner.split('_')[1]}_after_{rule_name}.json")
                    # 5 - Compare output
                    before, after = comparators.compare_checkov(
                        f"scan_results/{runner.split('_')[1]}_before_{rule_name}.json", f"scan_results/{runner.split('_')[1]}_after_{rule_name}.json")

                    print(runner.split('_')[1], before, after)
