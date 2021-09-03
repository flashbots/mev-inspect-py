load('ext://helm_remote', 'helm_remote')
helm_remote("postgresql",
            repo_name='bitnami',
            repo_url='https://charts.bitnami.com/bitnami',
            values=["k8s/postgresql/values_dev.yaml"]
)

docker_build('mev-inspect', '.',
    live_update=[
        sync('.', '/app'),
        run('cd /app && poetry install',
            trigger='./pyproject.toml'),
    ],
)

k8s_yaml("k8s/app.yaml")
