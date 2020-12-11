# Juju application for ML-NFV-EC

## Get started
Install dependencies
```
sudo snap install lxd
sudo snap install microk8s --classic
# Run the following 2 commands to use microk8s without sudo
sudo usermod -a -G microk8s davidf
sudo chown -f -R davidf ~/.kube
microk8s.enable dns storage # enable these two addons
sudo snap install juju --classic
sudo snap install charmcraft --channel beta
python3 -m pip install charmcraft # alternative and better command to install charmcraft
```


Prepare the environment (choose one).
Note: lxd and microk8s clouds are added by default when installing juju. 
- For microk8s
```
juju bootstrap microk8s <k8s-ctrl> # create controller for microk8s
juju add-model <model_name> <cloud-name>
juju switch <model-name>
juju switch <ctrl-name>
```

- For lxd
```
juju bootstrap localhost <lxd-ctrl> # create a controller for lxd
juju add-model <model_name> <cloud-name>
```

Kubernetes debug
```
microk8s.kubectl get namespaces
microk8s.kubectl get pods
microk8s.kubectl get all --all-namespaces
microk8s.kubectl get pods --namespace <namespace>
microk8s.kubectl --namespace <namespace> exec --stdin --tty <pod-name> -- /bin/bash # attach to console
microk8s.kubectl --namespace ml-test logs <pod_name>
```

LXD debug
```
lxc list
lxc exec <lxc-name> bash
```

Create, Build and deploy
```
charmcraft init --name mljuju --project-dir mljuju-operator
charmcraft build
juju deploy ./basic.charm
watch -c juju status --color
juju remove-application
```