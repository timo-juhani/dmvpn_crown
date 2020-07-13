from crown import Configuration

# Deploy spoke configuration to the target devices.

baseline_configuration = Configuration("router", "spoke", "baseline.j2")
baseline_configuration.run_nornir()
spoke_configuration = Configuration("router", "spoke", "dmvpn_spoke.j2")
spoke_configuration.run_nornir()
