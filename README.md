#  DMVPN Configuration with Nornir 

<img src="nornir.png" width="200">

This repository concentrates on automating the deployment of a multi-VRF DMVPN network. It's common for these networks to grow in number of spokes and VRFs. Sometimes so much that manageability takes a hit. Therefore, modeling the deployment as Infra as Code helps to mitigate these scaling issues and avoid mistakes when deploying or changing something in the existing deployment. It's also easy to re-run the scripts to make sure all configuration is as it should. Checking this manually each device at a time is time consuming to say the least.

To run the code:
- Clone the repository
- Launch a Python 3.x virtual environment (VENV): ```python -m venv .```
- Install dependencies: ```pip3 install -r requirements.txt```
- Adjust ```config_data``` with your own variables
- Execute the scripts:
    - ```python3 deploy_hubs.py```
    - ```python3 deploy_spokes.py```
