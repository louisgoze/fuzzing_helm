import yaml
import rules
import runners
import comparators
from benedict import benedict
import argparse
import os


def to_stdout(final_dict):
    print(yaml.safe_dump(final_dict))


def save_yaml(final_dict, filename):
    with open(filename, 'w') as outfile:
        outfile.write(final_dict.to_yaml())


def read_yaml(filename) -> dict:
    input_file = open(filename, "r")
    yaml_data = benedict(yaml.safe_load(input_file))
    return yaml_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Yaml fuzzer')
    parser.add_argument(
        '-f', '--file', help='Input YAML file to fuzz', type=str, required=True)
    parser.add_argument(
        '-o', '--output', help='Output fuzzed YAML file', type=str, default="output/output.yml")
    args = parser.parse_args()

    input_data = read_yaml(args.file)
    for name, fn in rules.__dict__.items():
        if callable(fn):
            # 1 - Run tools on the default yaml data
            runners.run_checkov(os.path.dirname(
                args.file), "checkov_before.json")
            print("Running fuzzer:", name)
            # 2 - Run your rules
            fuzzed_input = fn(input_data)
            save_yaml(fuzzed_input, args.output)
            # 3 - Run tools again on fuzzed yaml
            runners.run_checkov(os.path.dirname(
                args.output), "checkov_after.json")
            # 4 - Compare output
            before, after = comparators.compare_checkov(
                "checkov_before.json", "checkov_after.json")
            print("checkov", before, after)
