current_image=$(kubectl get deployment mev-inspect -o=jsonpath='{$.spec.template.spec.containers[:1].image}')

helm template mev-inspect-backfill ./k8s/mev-inspect-backfill \
    --set image.repository=$current_image \
    --set command.startBlockNumber=$1 \
    --set command.endBlockNumber=$2 | kubectl apply -f -
