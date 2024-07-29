import os
import subprocess

def apply_yaml_files(directory):
    successful_deployments = []
    yaml_files = [f for f in os.listdir(directory) if f.endswith('.yml')]
    for yaml_file in yaml_files:
        filepath = os.path.join(directory, yaml_file)
        try:
            result = subprocess.run(['microk8s', 'kubectl', 'apply', '-f', filepath], capture_output=True)
            print(f"Return code for {yaml_file}: {result.returncode}")
            if result.returncode == 0:
                successful_deployments.append(filepath)
        except Exception as e:
            print(f"Error applying {yaml_file}: {e}")
    return successful_deployments

def delete_successful_deployments(deployments):
    for deployment in deployments:
        try:
            subprocess.run(['microk8s', 'kubectl', 'delete', '-f', deployment], capture_output=True)
            print(f"Deleted successful deployment {deployment}.")
        except Exception as e:
            print(f"Error deleting deployment {deployment}: {e}")

def main():
    directory = "output/"
    successful_deployments = apply_yaml_files(directory)
    delete_successful_deployments(successful_deployments)

if __name__ == "__main__":
    main()
