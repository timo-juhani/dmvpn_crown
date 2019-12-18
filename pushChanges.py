from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_title, print_result
import yaml
import jinja2

def changeConfig(task):
    # Load the template
    r = task.run(task=text.template_file, 
                name="Loading the change template.", 
                template="changes.j2", 
                path=f"templates/")

    # Save the rendered configuration
    task.host["config"] = r.result

    # Deploy the configuration
    task.run(task=networking.napalm_configure,
            name="Loading the changes on the devices.",
            replace=False,
            configuration=task.host["config"])

# Execute 

nr = InitNornir(config_file="config.yaml")
routers = nr.filter(type="router")
spokes = nr.filter(type="router", role="spoke")
hubs = nr.filter(type="router", role="hub")

print_title("Gathering the facts.")

# Gather facts about the devices
r = routers.run(task=networking.napalm_get, getters=["facts"])
print_result(r)

print_title("Configuring the network")

# Run configuration changes
r = routers.run(task=changeConfig)
print_result(r)