from crown import Configuration

# Deploy hub configuration to the target devices.

baseline_configuration = Configuration("router", "hub", "baseline.j2")
baseline_configuration.run_nornir()
hub_configuration = Configuration("router", "hub", "dmvpn_hub.j2")
hub_configuration.run_nornir()
