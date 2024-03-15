import copy


def fuzz_ssh_port(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].ports[0].containerPort"] = 22
    return output_dict
    
def fuzz_memory_limit(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].resources.limits.memory"] = "0m"
    return output_dict


def fuzz_memory_request(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].resources.requests.memory"] = "0Mi"
    return output_dict

def fuzz_cpu_limit(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].resources.limits.cpu"] = "0.005"
    return output_dict


def fuzz_cpu_request(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].resources.requests.cpu"] = "0.00"
    return output_dict

def fuzz_imagePullPolicy(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].imagePullPolicy"] = "~Always"
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

def fuzz_securityContext_3(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].securityContext.capabilities"] = {}
    return output_dict


def fuzz_securityContext_4(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].securityContext.capabilities"] = {
        'add': ["NET_ADMIN", "SYS_TIME"], 'drop': ["ALL"]}
    return output_dict


def fuzz_seccomp_profile(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].securityContext.seccompProfile.type"] = "Unconfined"
    return output_dict

def fuzz_command(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].command"] = ["netcat", "-nvlp", "8888"]
    return output_dict

def fuzz_readOnlyRootFilesystem(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].securityContext.readOnlyRootFilesystem"] = False
    return output_dict

def fuzz_privileged(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].securityContext.privileged"] = True
    return output_dict

def fuzz_allowPrivilegeEscalation(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].securityContext.allowPrivilegeEscalation"] = True
    return output_dict

def fuzz_runAsNonRoot(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].securityContext.runAsNonRoot"] = False
    return output_dict

def fuzz_automountServiceAccountToken(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.automountServiceAccountToken"] = True
    return output_dict

def fuzz_command2(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].livenessProbe.exec"] = { 
        'command': ["netcat", "-nvlp", "8888"]}
    return output_dict

def fuzz_ressources(input_dict) -> dict:
    output_dict = copy.deepcopy(input_dict)
    output_dict["spec.template.spec.containers[0].resources.requests.cpu"] = "0.00"
    output_dict["spec.template.spec.containers[0].resources.limits.cpu"] = "0.00"
    return output_dict
