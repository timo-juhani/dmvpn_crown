from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_title, print_result
import yaml
import jinja2

def pushBaseline(task):
    # Push same configuration on all devices that has type router
    r = task.run(task=text.template_file, 
                name="Push baseline configuration", 
                template="baseline.j2", 
                path=f"templates/")

    # Saving the configuration that was rendered
    task.host["config"] = r.result

    # Napalm deploys the configuration to the devices
    task.run(task=networking.napalm_configure,
            name="Loading Configuration on the device",
            replace=False,
            configuration=task.host["config"])

def pushDmvpnSpoke(task):

    # Open the configuration file dedicated for the router
    with open(f'config_data/{task.host["site"]}.yaml') as file:
        config_data = yaml.load(file, Loader=yaml.FullLoader)

    # Render the IOS configuration
    templateLoader = jinja2.FileSystemLoader(searchpath="templates/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    t = "dmvpn_spoke.j2"
    template = templateEnv.get_template(t)
    config = template.render(config_data)
    print(config)

    # Push the configuration to the device
    task.run(task=networking.napalm_configure, 
            name="Pushing the spoke configuration",
            replace=False,
            configuration=config)

def pushDmvpnHub(task):

    # Open the configuration file dedicated for the router
    with open(f'config_data/{task.host["site"]}.yaml') as file:
        config_data = yaml.load(file, Loader=yaml.FullLoader)

    # Render the IOS configuration
    templateLoader = jinja2.FileSystemLoader(searchpath="templates/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    t = "dmvpn_hub.j2"
    template = templateEnv.get_template(t)
    config = template.render(config_data)

    # Push the configuration to the device
    task.run(task=networking.napalm_configure, 
            name="Pushing the hub configuration",
            replace=False,
            configuration=config)

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

# Execute 

nr = InitNornir(config_file="config.yaml")
routers = nr.filter(type="router")
spokes = nr.filter(type="router", role="spoke")
hubs = nr.filter(type="router", role="hub")

print_title("Gathering the facts.")

# Gather facts about the devices
# r = routers.run(task=networking.napalm_get, getters=["facts"])
# print_result(r)

print_title("Configuring the network")

# Apply the baseline configuration
# r = hubs.run(task=pushBaseline)
# print_result(r)

# Push the DMVPN hub configurations
# r = hubs.run(task=pushDmvpnHub)
# print_result(r)

# # Push the DMVPN spoke configurations
r = spokes.run(task=pushDmvpnSpoke)
print_result(r)

# # Run configuration changes
# r = routers.run(task=changeConfig)
# print_result(r)