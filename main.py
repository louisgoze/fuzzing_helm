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
    runners.run_checkov(
        args.file, f"checkov_before_base.json")
    print("Running fuzzer:", "base")
    # 2 - Run your rules
    output_name = "output/output_base.yml"
    save_yaml(input_data, output_name)
    # 3 - Run tools again on fuzzed yaml
    runners.run_checkov(
        output_name, f"checkov_after_base.json")
    # 4 - Compare output
    before, after = comparators.compare_checkov(
        f"checkov_before_base.json", f"checkov_after_base.json")
    print("checkov", before, after)

    for name, fn in rules.__dict__.items():
        if callable(fn):
            # 1 - Run tools on the default yaml data
            input_data = read_yaml(args.file)
            runners.run_checkov(
                args.file, f"checkov_before_{name}.json")
            print("Running fuzzer:", name)
            # 2 - Run your rules
            fuzzed_input = fn(input_data)
            assert fuzzed_input != input_data
            output_name = "output/output_" + name + ".yml"
            save_yaml(fuzzed_input, output_name)
            # 3 - Run tools again on fuzzed yaml
            runners.run_checkov(
                output_name, f"checkov_after_{name}.json")
            # 4 - Compare output
            before, after = comparators.compare_checkov(
                f"checkov_before_{name}.json", f"checkov_after_{name}.json")
            print("checkov", before, after)
