
### Local setup

Requirements:

* python3 and pip3

Instructions: 

* Setup a virtual enviroment to manage dependencies (optional)  
    * `python3 -m venv env`
* Activate it
    * `. env/bin/activate` (exit with `deactivate`)
* web3 build-related dependencies (on Ubuntu 20.04)
    * `sudo apt-get install libevent-dev libpython3.8-dev python3.8-dev libssl-dev`
* Install python libraries
    * `pip3 install -r requirements.txt`
* Run tests for token flow
    * `python -m unittest tests/tokenflow_test.py`
