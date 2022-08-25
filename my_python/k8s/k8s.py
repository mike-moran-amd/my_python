"""
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list

sudo apt update
sudo apt install -y containerd.io

wget https://github.com/opencontainers/runc/releases/download/v1.1.1/runc.amd64
sudo install -m 755 runc.amd64 /usr/local/sbin/runc

sudo mkdir -p /etc/containerd/

containerd config default | sudo tee /etc/containerd/config.toml

sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml

sudo systemctl restart containerd

cat <<EOF | sudo tee -a /etc/containerd/config.toml
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
SystemdCgroup = true
EOF

sudo sed -i 's/^disabled_plugins \=/\#disabled_plugins \=/g' /etc/containerd/config.toml

sudo systemctl restart containerd

sudo ufw allow 6443/tcp
sudo ufw allow 2379/tcp
sudo ufw allow 2380/tcp
sudo ufw allow 10250/tcp
sudo ufw allow 10257/tcp
sudo ufw allow 10259/tcp
sudo ufw reload
sudo ufw allow 10250/tcp
sudo ufw allow 30000:32767/tcp
sudo ufw reload

cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

sudo sysctl --system

sudo swapoff -a
sudo nano /etc/fstab

sudo modprobe br_netfilter

sudo sysctl net.bridge.bridge-nf-call-iptables=1

sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list


sudo apt update
sudo apt install -y kubelet kubeadm kubectl

sudo kubeadm init --pod-network-cidr=192.168.0.0/16

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

kubectl taint nodes --all node-role.kubernetes.io/master-
kubectl taint nodes --all node-role.kubernetes.io/control-plane-

kubectl create -f https://projectcalico.docs.tigera.io/manifests/tigera-operator.yaml
kubectl create -f https://projectcalico.docs.tigera.io/manifests/custom-resources.yaml

----------------------------------

kubeadm reset
sudo apt-get purge kubeadm kubectl kubelet kubernetes-cni kube*
sudo apt-get autoremove
sudo rm -rf ~/.kube

 ctr -n=k8s.io images import <filename-from-previous-step>


FROM ubuntu:22.04
RUN apt-get -y update
RUN apt-get install -y sysbench
CMD sysbench cpu --cpu-max-prime=200000 --events=20000 --time=0 --threads=1 run

10.216.178.175
"""

HISTORY="""
mfm@mm74:/home/mfm/weathervane$ history
    1  sudo apt update
    2  sudo apt install -y ca-certificates curl gnupg lsb-release
    3  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    4  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list
    5  sudo apt update
    6  sudo apt install -y containerd.io
    7  wget https://github.com/opencontainers/runc/releases/download/v1.1.1/runc.amd64
    8  sudo install -m 755 runc.amd64 /usr/local/sbin/runc
    9  sudo mkdir -p /etc/containerd/
   10  containerd config default | sudo tee /etc/containerd/config.toml
   11  sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml
   12  sudo sed -i 's/^disabled_plugins \=/\#disabled_plugins \=/g' /etc/containerd/config.toml
   13  sudo systemctl restart containerd
   14  sudo ufw allow 6443/tcp
   15  sudo ufw allow 2379/tcp
   16  sudo ufw allow 2380/tcp
   17  sudo ufw allow 10250/tcp
   18  sudo ufw allow 10257/tcp
   19  sudo ufw allow 10259/tcp
   20  sudo ufw reload
   21  sudo ufw allow 10250/tcp
   22  sudo ufw allow 30000:32767/tcp
   23  sudo ufw reload
   24  cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

   25  cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

   26  sudo sysctl --system
   27  sudo swapoff -a
   28  sudo vi /etc/fstab  # comment out swap line
   29  sudo cat /etc/fstab
   30  sudo modprobe br_netfilter
   31  sudo sysctl net.bridge.bridge-nf-call-iptables=1
   32  sudo apt update
   33  sudo apt install -y apt-transport-https ca-certificates curl
   34  sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
   35  echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
   36  sudo apt update
   37  sudo apt install -y kubelet kubeadm kubectl
   38  sudo kubeadm init --pod-network-cidr=192.168.0.0/16
   39  mkdir -p $HOME/.kube
   40  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
   41  sudo chown $(id -u):$(id -g) $HOME/.kube/config
   42  kubectl taint nodes --all node-role.kubernetes.io/master-
   43  kubectl taint nodes --all node-role.kubernetes.io/control-plane-
   44  kubectl create -f https://projectcalico.docs.tigera.io/manifests/tigera-operator.yaml
   45  kubectl create -f https://projectcalico.docs.tigera.io/manifests/custom-resources.yaml
   46  kubectl get nodes --show-labels
   47  sudo mkdir -p /k8s/weathervane/vol
   48  sudo chmod -R 777 /k8s
   49  git clone http://github.com/vmware/weathervane
   50  cd weathervane/
   51  cat > create-persistent-vol.yaml << EOF
apiVersion: v1
kind: PersistentVolume
metadata:
  name: weathervane-pv
spec:
  capacity:
    storage: 400Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  local:
    path: /k8s/weathervane/vol
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - mm74
EOF

   52  kubectl create -f create-persistent-vol.yaml
   53  kubectl get pv
   54  cat > create-storage-class.yaml << EOF
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: Immediate
EOF

   55  kubectl create -f create-storage-class.yaml
   56  kubectl get sc
   57  cat > weathervane.config.k8s.quickstart << EOF
{
  "description" : "micro",
  "configurationSize": "micro",
  "runStrategy" : "fixed",
  "dockerNamespace" : "mikemoranamd",
  "kubernetesClusters" : [
    {
      "name" : "kubernetes",
      "kubeconfigFile" : "/home/mfm/.kube/config",
      "kubeconfigContext" : "",
    },
  ],
  "driverCluster" : "kubernetes",
  "appInstanceCluster" : "kubernetes",
  "appIngressMethod" : "clusterip",
  "cassandraDataStorageClass" : "local-storage",
  "postgresqlStorageClass" : "local-storage",
  "nginxCacheStorageClass" : "local-storage",
}
EOF

   58  cat create-persistent-vol.yaml
   59  cat create-storage-class.yaml
   60  cat weathervane.config.k8s.quickstart
   61  sudo ./runWeathervane.pl --configFile=weathervane.config.k8s.quickstart
   62  ./runWeathervane.pl --configFile=weathervane.config.k8s.quickstart
   63  history
"""

# ssh root@ip_address
ROOT_SCRIPT = """
useradd -s /bin/bash -d /home/mfm/ -m -G sudo mfm
passwd mfm
cp -r ~/.ssh /home/mfm/.ssh
chown -R mfm:mfm /home/mfm/.ssh
exit
"""

# ssh user@ip_address
USER_SCRIPT = """
sudo apt update  # this will prompt for password set in ROOT_SCRIPT (above)
sudo apt install -y ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt update
sudo apt install -y containerd.io
wget https://github.com/opencontainers/runc/releases/download/v1.1.1/runc.amd64
sudo install -m 755 runc.amd64 /usr/local/sbin/runc
sudo mkdir -p /etc/containerd/
containerd config default | sudo tee /etc/containerd/config.toml
sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml
sudo sed -i 's/^disabled_plugins \=/\#disabled_plugins \=/g' /etc/containerd/config.toml
sudo systemctl restart containerd
sudo ufw allow 6443/tcp
sudo ufw allow 2379/tcp
sudo ufw allow 2380/tcp
sudo ufw allow 10250/tcp
sudo ufw allow 10257/tcp
sudo ufw allow 10259/tcp
sudo ufw reload
sudo ufw allow 10250/tcp
sudo ufw allow 30000:32767/tcp
sudo ufw reload
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

sudo sysctl --system
sudo swapoff -a
sudo vi /etc/fstab  # comment out swap line
sudo cat /etc/fstab
sudo modprobe br_netfilter
sudo sysctl net.bridge.bridge-nf-call-iptables=1
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt update
sudo apt install -y kubelet kubeadm kubectl


sudo kubeadm init --pod-network-cidr=192.168.0.0/16
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
kubectl taint nodes --all node-role.kubernetes.io/master-
kubectl taint nodes --all node-role.kubernetes.io/control-plane-
kubectl create -f https://projectcalico.docs.tigera.io/manifests/tigera-operator.yaml
kubectl create -f https://projectcalico.docs.tigera.io/manifests/custom-resources.yaml
kubectl get nodes --show-labels

sudo mkdir -p /k8s/weathervane/vol
sudo chmod -R 777 /k8s
git clone http://github.com/vmware/weathervane
cd weathervane/
cat > create-persistent-vol.yaml << EOF
apiVersion: v1
kind: PersistentVolume
metadata:
  name: weathervane-pv
spec:
  capacity:
    storage: 400Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  local:
    path: /k8s/weathervane/vol
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - mm74
EOF

   52  kubectl create -f create-persistent-vol.yaml
   53  kubectl get pv
   54  cat > create-storage-class.yaml << EOF
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: Immediate
EOF

   55  kubectl create -f create-storage-class.yaml
   56  kubectl get sc
   57  cat > weathervane.config.k8s.quickstart << EOF
{
  "description" : "micro",
  "configurationSize": "micro",
  "runStrategy" : "fixed",
  "dockerNamespace" : "mikemoranamd",
  "kubernetesClusters" : [
    {
      "name" : "kubernetes",
      "kubeconfigFile" : "/home/mfm/.kube/config",
      "kubeconfigContext" : "",
    },
  ],
  "driverCluster" : "kubernetes",
  "appInstanceCluster" : "kubernetes",
  "appIngressMethod" : "clusterip",
  "cassandraDataStorageClass" : "local-storage",
  "postgresqlStorageClass" : "local-storage",
  "nginxCacheStorageClass" : "local-storage",
}
EOF

   58  cat create-persistent-vol.yaml
   59  cat create-storage-class.yaml
   60  cat weathervane.config.k8s.quickstart
   61  sudo ./runWeathervane.pl --configFile=weathervane.config.k8s.quickstart
   62  ./runWeathervane.pl --configFile=weathervane.config.k8s.quickstart
   63  history
"""
