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
    runners.run_checkov(
        args.file, f"scan_results/checkov_before_base.json")
    print("Running fuzzer:", "base")
    # 2 - Run your rules
    output_rule_name = "output/output_base.yml"
    save_yaml(input_data, output_rule_name)
    # 3 - Run tools again on fuzzed yaml
    runners.run_checkov(
        output_rule_name, f"scan_results/checkov_after_base.json")
    # 4 - Compare output
    before, after = comparators.compare_checkov(
        f"scan_results/checkov_before_base.json", f"scan_results/checkov_after_base.json")
    print("checkov", before, after)

    for rule_name, fn in rules.__dict__.items():
        if callable(fn):
            output_rule_name = "output/output_" + rule_name + ".yml"
            # 1 - Run tools on the default yaml data
            print("Running fuzzer:", rule_name)
            for runner, runner_fn in runners.__dict__.items():
                if callable(runner_fn):
                    runner_fn(
                        args.file, f"scan_results/{runner.split('_')[1]}_before_{rule_name}.json")

                    # 2 - Run your rules
                    fuzzed_input = fn(input_data)
                    assert fuzzed_input != input_data
                    save_yaml(fuzzed_input, output_rule_name)
                    # 3 - Run tools again on fuzzed yaml
                    runner_fn(
                        args.file, f"scan_results/{runner.split('_')[1]}_after_{rule_name}.json")
                    # 4 - Compare output
                    before, after = comparators.compare_checkov(
                        f"scan_results/{runner.split('_')[1]}_before_{rule_name}.json", f"scan_results/{runner.split('_')[1]}_after_{rule_name}.json")
                    print(runner.split('_')[1], before, after)
