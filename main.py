import yaml
import rules
import runners
import comparators
from benedict import benedict
import argparse


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
                        args.file, f"scan_results/{runner.split('_')[1]}_after_{rule_name}.json")
        else:
            continue
        for comparator_name, comparator_fn in comparators.__dict__.items():
            if callable(comparator_fn):
                before, after = comparator_fn(
                    f"scan_results/{comparator_name.split('_')[1]}_before_{rule_name}.json", f"scan_results/{comparator_name.split('_')[1]}_after_{rule_name}.json")

                print(comparator_name.split('_')[1], before, after)
