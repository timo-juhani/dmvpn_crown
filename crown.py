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
        site = task.host["site"]
        config_data = self.open_config(task)
        templateLoader = jinja2.FileSystemLoader(searchpath="templates/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        t = self.template
        template = templateEnv.get_template(t)
        print_title(f"Rendering configuration: {self.template} on {site}.")
        config = template.render(config_data)
        print(config)
        return config, site

    def save_config(self, task):
        config, site = self.render_config(task)
        print_title(f"Saving configuration to: output/{site}.conf.")
        try:
            with open(f'output/{site}.conf', "a") as file:
                file.write(config)
                file.close()
            print("[+] Done")
        except Exception as e:
            print(f"[-] An Error occured: {e}")

    def deploy_config(self, task):
        config, site = self.render_config(task)
        print_title(f"Configuring {self.template} on {site}.")
        try:
            task.run(task=networking.napalm_configure,
                     name="Loading Configuration on the device",
                     replace=False,
                     configuration=config)
            print("[+] Done")
        except Exception as e:
            print(f"[-] An Error occured: {e}")

    def run_nornir(self):
        nr = InitNornir(config_file="config.yaml")
        devices = nr.filter(type=self.type, role=self.role)
        prompt = "[!] DEPLOY(d) or SAVE(s) configuration. " + \
            "Use QUIT(q) if you need to exit: "
        option = input(prompt)

        if option in ["DEPLOY", "d"]:
            devices.run(task=self.deploy_config)

        elif option in ["SAVE", "s"]:
            devices.run(task=self.save_config)

        elif option in ["QUIT", "q"]:
            print("[+] Exiting.")
            exit(0)
        else:
            print("[-] Error! Not a valid input.")
