import copy


def fuzz_ssh_port(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].ports[0].containerPort"] = 22
    return output_dict


def fuzz_memory_limit(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].resources.limits.memory"] = "0m"
    return output_dict
    # "spec/template/spec/containers/[0]/resources/limits/memory"
