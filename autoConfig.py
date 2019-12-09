from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_title, print_result

nr = InitNornir(config_file="config.yaml")

routers = nr.filter(type="router", role="sandbox")
print_title("Gathering the facts.")
result = routers.run(task=networking.napalm_get, getters=["facts"])
print_result(result)

def applyBaseline(task):
    # Push same configuration on all devices that has type router
    r = task.run(task=text.template_file, 
                name="Apply Baseline Configuration", 
                template="baseline.j2", 
                path=f"templates/")

    # Saving the configuration that was rendered
    task.host["config"] = r.result

    # Napalm deploys the configuration to the devices
    task.run(task=networking.napalm_configure,
            name="Loading Configuration on the device",
            replace=False,
            configuration=task.host["config"])

def changeConfig(task):
    # Modify the configuration based on "changes.j2" template
    r = task.run(task=text.template_file, 
                name="Loading the change template.", 
                template="changes.j2", 
                path=f"templates/")

    # Saving the configuration that was rendered
    task.host["config"] = r.result

    # Napalm deploys the configuration to the devices
    task.run(task=networking.napalm_configure,
            name="Loading the changes on the devices.",
            replace=False,
            configuration=task.host["config"])

print_title("Configuring the network")

# Run configuration changes
result = routers.run(task=changeConfig)
print_result(result)

# Apply the baseline configuration
result = routers.run(task=applyBaseline)
print_result(result)