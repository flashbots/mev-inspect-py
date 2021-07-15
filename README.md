
### Local setup

Requirements:

* python3 and pip3

Instructions to run: 

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

If contributing:
* Install dev libraries
    * `pip3 install -r requirements_dev.txt`
* Setup pre-commit
    * `pre-commit install`
* Install dependencies and verify it's working
    * `pre-commit run --all-files`
    * If you see "failed to find interpreter for..." it means you're missing the correct python version
    * The current version is python3.9 - [pyenv](https://github.com/pyenv/pyenv) is a great option for managing python versions
