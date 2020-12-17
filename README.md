# Juju application for ML-NFV-EC

## Get started
Install dependencies
```
sudo snap install lxd
sudo snap install microk8s --classic

# Run the following 2 commands to use microk8s without sudo
sudo usermod -a -G microk8s davidf
sudo chown -f -R davidf ~/.kube

# Reload bash terminal
microk8s.enable dns storage # enable these two addons
sudo snap install juju --classic

# Install charmcraft using one of the following commands (using pip is better)
sudo snap install charmcraft --channel beta
python3 -m pip install charmcraft
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

## Using Juju
Create, build and deploy
```
charmcraft init --name mljuju --project-dir mljuju-operator
charmcraft build
python3 -m charmcraft build # if you installed charmcraft with python
juju deploy ./mljuju.charm
```

Relations
```
juju add-relation <charm1> <charm2>
```

Remove data
```
juju remove-application <app>
juju remove-application <app> --force

juju remove-relation <charm1> <charm2>
```

Get ip addres (and other data) directly from relation data
- Relation data object
```
```

- Code to extract data

```python
def get_ip_addr(self, event):
    if event.unit in event.realtion.data:
        data = event.relation.data[event.unit]
        ip_addr = data.get("ingress-address")
        port = data.get("port")
        host = data.get("host")
```

## Debugging
Juju debug (recommended)
```
watch -c juju status --color

juju debug-log --include <app> --replay

juju debug-hooks <app>/0
juju debug-hook <app> start # start is the hook name

juju debug-hooks <app>/0
$ ./dispatch
$ vim src/charm.py # import pdb; pdb.set.trace()
juju resolve <app>/0
```

Kubernetes sepcific debug
```
microk8s.kubectl get namespaces
microk8s.kubectl get pods
microk8s.kubectl get all --all-namespaces
watch -c microk8s.kubectl get pods --namespace <namespace>

microk8s.kubectl --namespace <namespace> exec --stdin --tty <pod-name> -- /bin/bash # attach to console

microk8s.kubectl --namespace ml-test logs <pod_name>
```

LXD specific debug
```
watch -c lxc list
lxc exec <lxc-name> bash
```

## Juju concepts
- A single juju controller manages multiple models
- Each model has one or more applications (charms)
- Each application has one or more machines
- We use the term `operator` to refer to the charm code and `workload` to refer to the target app code
- The following table shows the mapping between OSM/Openstack and Juju concepts

|    Juju     | OSM/Openstack |
|-------------|---------------|
| Model       | NS            |
| Application | VNF           |
| Machine     | VDU           |

- Two modes to work with Juju: Kubernets vs LXD
 
```
+-----------------------------------------------+
|                                               |
|  +----------------+       +----------------+  |
|  |    Operator    |       |    Workload    |  |
|  |    (charm)     |       |   (app code)   |  |
|  |                |       |                |  |
|  |  *image of the |-------|                |  |
|  |   configured   |       |                |  |
|  |   workload     |       |                |  |
|  +----------------+       +----------------+  |
|                                               |
|  Kubernetes                                   |
+-----------------------------------------------+


+------------------------------+
|                              |
|   +----------------------+   |
|   |  +----------------+  |   |
|   |  |    Operator    |  |   |
|   |  |    (charm)     |  |   |
|   |  |                |  |   |
|   |  +----------------+  |   |
|   |                      |   |
|   |       Workload       |   |
|   |      (app code)      |   |
|   +----------------------+   |
|                              |
|   LXD / VNF                  |
+------------------------------+
```

The standard deplyment of a charm in Kubernetes reqiures the deployment of two pods, one with the charm code called Operator and the associated Workload pod (as shown above). If you work with Proxy Charms is juju, you will use the following option (in `metadata.yaml`) so that only the Operator charm pod is deployed (withoud the associated workload).
```yaml
deployment:
  mode: operator
```