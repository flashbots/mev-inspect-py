# Helm Remote

Author: [Bob Jackman](https://github.com/kogi)

Install a remotely hosted Helm chart in a way that it will be properly uninstalled when running `tilt down`

## Usage

#### Install a Remote Chart

```py
load('ext://helm_remote', 'helm_remote')
helm_remote('myChartName')
```

##### Additional Parameters

```
helm_remote(chart, repo_url='', repo_name='', release_name='', namespace='', version='', username='', password='', values=[], set=[])
```

* `chart` ( str ) – the name of the chart to install  
* `repo_name` ( str ) – the name of the repo within which to find the chart (assuming the repo is already added locally)
<br> if omitted, defaults to the same value as `chart_name`
* `repo_url` ( str ) – the URL of the repo within which to find the chart (equivalent to `helm repo add <repo_name> <repo_url>`)
* `release_name` (str) - the name of the helm release
<br> if omitted, defaults to the same value as `chart_name`
* `namespace` ( str ) – the namespace to deploy the chart to (equivalent to helm's `--namespace <namespace>` flags)
* `version` ( str ) – the version of the chart to install. If omitted, defaults to latest version (equivalent to helm's `--version` flag)
* `username` ( str ) – repository authentication username, if needed (equivalent to helm's `--username` flag)
* `password` ( str ) – repository authentication password, if needed (equivalent to helm's `--password` flag)
* `values` ( Union [ str , List [ str ]]) – Specify one or more values files (in addition to the values.yaml file in the chart). Equivalent to the helm's `--values` or `-f` flags
* `set` ( Union [ str , List [ str ]]) – Directly specify one or more values (equivalent to helm's `--set` flag)
* `allow_duplicates` ( bool ) - Allow duplicate resources. Usually duplicate resources indicate a programmer error.
   But some charts specify resources twice.
* `create_namespace` ( bool ) - Create the namespace specified in `namespace` ( equivalent to helm's `--create_namespace` flag)

#### Change the Cache Location

By default `helm_remote` will store retrieved helm charts in the `.helm` directory at your workspace's root.
This location can be customized by calling `os.putenv('TILT_HELM_REMOTE_CACHE_DIR', new_directory)` before loading the module.
