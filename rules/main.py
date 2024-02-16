import copy


def fuzz_ssh_port(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].ports[0].containerPort"] = 22
    return output_dict
    
def fuzz_memory_limit(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].resources.limits.memory"] = "0m"
    return output_dict

def fuzz_cpu_limit(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].resources.limits.cpu."] = "0,5m"
    return output_dict

def fuzz_imagePullPolicy(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].imagePullPolicy"] = "Alwayss"
    return output_dict

def fuzz_group(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].securityContext.runAsGroup"] = 1
    return output_dict

#def fuzz_sha(input_dict) -> dict:
#    output_dict = copy.deepcopy(input_dict)
#    output_dict["spec.template.spec.containers[0].image"] = "nginx:1.14.2@sha256:88"
#    return output_dict

def fuzz_sha(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].image"] = "nginx:1.36.2@sha256:88"
    return output_dict

def fuzz_securityContext(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].securityContext.readOnlyRootFilesystem"] = False
    return output_dict

def fuzz_drop(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].securityContext.capabilities.drop[0]"] = "NONE"
    return output_dict

def fuzz_runAsUser(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].securityContext.runAsUser"] = -2000
    return output_dict

def fuzz_PrivilegeEscalation(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].securityContext.allowPrivilegeEscalation"] = True
    return output_dict

def fuzz_RootFilesystem(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].securityContext.readOnlyRootFilesystem"] = False
    return output_dict
