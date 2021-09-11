load('ext://helm_remote', 'helm_remote')
helm_remote("postgresql",
            repo_name='bitnami',
            repo_url='https://charts.bitnami.com/bitnami',
            set=["postgresqlPassword=password", "postgresqlDatabase=mev_inspect"],
)

load('ext://secret', 'secret_from_dict')
k8s_yaml(secret_from_dict("mev-inspect-db-credentials", inputs = {
    "username" : "postgres",
    "password": "password",
}))

docker_build('mev-inspect-py', '.',
    live_update=[
        sync('.', '/app'),
        run('cd /app && poetry install',
            trigger='./pyproject.toml'),
    ],
)

k8s_yaml("k8s/app.yaml")
