from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_title, print_result
import yaml
import jinja2


class Configuration:
    def __init__(self, type, role, template):
        self.type = type
        self.role = role
        self.template = template

    def open_config(self, task):
        with open(f'config_data/{task.host["site"]}.yaml') as file:
            config_data = yaml.load(file, Loader=yaml.FullLoader)
        return config_data

    def render_config(self, task):
        config_data = self.open_config(task)
        templateLoader = jinja2.FileSystemLoader(searchpath="templates/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        t = self.template
        template = templateEnv.get_template(t)
        config = template.render(config_data)
        return config

    def deploy_config(self, task):
        print_title(f"Configuring {self.template} on {task.host['site']}.")
        config = self.render_config(task)
        task.run(task=networking.napalm_configure,
                 name="Loading Configuration on the device",
                 replace=False,
                 configuration=config)

    def run_nornir(self):
        nr = InitNornir(config_file="config.yaml")
        devices = nr.filter(type=self.type, role=self.role)
        r = devices.run(task=self.deploy_config)
        return print_result(r)
