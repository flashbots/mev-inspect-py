# Configmap

Author: [Nick Santos](https://github.com/nicks)

Helper functions for creating Kubernetes configmaps.

## Functions

### configmap_yaml

```
configmap_yaml(name: str, namespace: str = "", from_file: Union[str, List[str]] = None, watch: bool = True, from_env_file: str = None): Blob
```

Returns YAML for a config map generated from a file.

* `from_file` ( str ) – equivalent to `kubectl create configmap --from-file`
* `from_env_file` (str) - equivalent to `kubectl create configmap --from-env-file`
* `watch` ( bool ) - auto-reload if the files change

### configmap_create

```
configmap_create(name: str, namespace: str = "", from_file: Union[str, List[str]] = None, watch: bool = True, from_env_file: str = None)
```

Deploys a config map. Equivalent to

```
k8s_yaml(configmap_yaml('name', from_file=[...]))
```

### configmap_from_dict

```
configmap_from_dict(name: str, namespace: str = "", inputs: Dict[str, str]] = None): Blob
```

Returns YAML for a config map generated from a given dictionary. Nested dictionaries are not supported

* `inputs` ( dict ) – equivalent to `kubectl create configmap --from-literal` for each key and value

## Example Usage

### For a Grafana config

```
load('ext://configmap', 'configmap_create')
configmap_create('grafana-config', from_file=['grafana.ini=./grafana.ini'])
```

## Caveats

- This extension doesn't do any validation to confirm that names or namespaces are valid.
