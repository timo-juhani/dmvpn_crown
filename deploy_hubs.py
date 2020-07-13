from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_title, print_result
import yaml
import jinja2


def pushBaseline(task):
    # Open the configuration file
    with open(f'config_data/{task.host["site"]}.yaml') as file:
        config_data = yaml.load(file, Loader=yaml.FullLoader)

    # Render the IOS configuration
    templateLoader = jinja2.FileSystemLoader(searchpath="templates/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    t = "baseline.j2"
    template = templateEnv.get_template(t)
    config = template.render(config_data)
    print(config)

    # Deploy the configuration
    task.run(task=networking.napalm_configure,
             name="Loading Configuration on the device",
             replace=False,
             configuration=config)


def pushDmvpnHub(task):

    # Open the configuration file
    with open(f'config_data/{task.host["site"]}.yaml') as file:
        config_data = yaml.load(file, Loader=yaml.FullLoader)

    # Render the IOS configuration
    templateLoader = jinja2.FileSystemLoader(searchpath="templates/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    t = "dmvpn_hub.j2"
    template = templateEnv.get_template(t)
    config = template.render(config_data)

    # Deploy the configuration
    task.run(task=networking.napalm_configure,
             name="Pushing the hub configuration",
             replace=False,
             configuration=config)

# Execute


nr = InitNornir(config_file="config.yaml")
hubs = nr.filter(type="router", role="hub")

print_title("Gathering the facts.")

# Gather facts about the devices
# r = routers.run(task=networking.napalm_get, getters=["facts"])
# print_result(r)

print_title("Configuring the hubs")

# Apply the baseline configuration
r = hubs.run(task=pushBaseline)
print_result(r)

# Push the DMVPN hub configurations
r = hubs.run(task=pushDmvpnHub)
print_result(r)
