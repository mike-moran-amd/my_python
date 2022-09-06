"""
>>> pprint.pprint(PATH_CONTENTS)
{'$HOME/.kube/config': None,
 '/etc/apt/sources.list.d/docker.list': None,
 '/etc/apt/sources.list.d/kubernetes.list': None,
 '/etc/containerd/config.toml': None,
 '/etc/containers/registries.conf': None,
 '/etc/fstab': None,
 '/etc/modules-load.d/k8s.conf': None,
 '/etc/sysctl.d/k8s.conf': None,
 '/usr/local/sbin/runc': None,
 '/usr/share/keyrings/docker-archive-keyring.gpg': None}

"""
import pprint
from my_python import data

TOUCHED_PATHS = [
    "/usr/share/keyrings/docker-archive-keyring.gpg",
    "/etc/apt/sources.list.d/docker.list",
    "/usr/local/sbin/runc",
    "/etc/containerd/config.toml",  # SystemCgroup = true  #disabled_plugins
    "/etc/modules-load.d/k8s.conf",  # br_netfilter
    "/etc/sysctl.d/k8s.conf",  # net.bridge.bridge-nf-call-ip6tables = 1
                               # net.bridge.bridge-nf-call-iptables = 1
                               # net.ipv4.ip_forward = 1
    "/etc/fstab",  # comment out swap line
    "/etc/apt/sources.list.d/kubernetes.list",
    "$HOME/.kube/config",
    "/etc/containers/registries.conf",  # append unqualified-search-registries=["docker.io"]
]

PATH_CONTENTS = {k: data.Content(k).content for k in TOUCHED_PATHS}


COMMANDS_TODO = [
    "podman-compose up",
    "sudo apt install mlocate",
    "locate Term/ReadKey.pm",
    "podman-compose up",
    "sudo cpan Term::ReadKey",
    "cpan",
    "kubectl get events --all-namespaces",  # 1 pod has unbound immediate PersistentVolumeClaims
    "kubectl get deployments",

]


UBUNTU_2004_INSTALL_SCRIPT = """
uname -a  # should be Ubuntu 20.04 or RAISE
apt-get update
apt-get -y upgrade <<EOF
Y
EOF

apt install -y build-essential curl gnupg2 software-properties-common apt-transport-https ca-certificates
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt update
apt upgrade -y
apt install -y docker-ce containerd.io
swapoff -a
mkdir -p /etc/containerd
containerd config default > /etc/containerd/config.toml
systemctl restart containerd
systemctl enable containerd
curl -LO https://golang.org/dl/go1.18.1.linux-amd64.tar.gz
tar -C /usr/local -xzf go1.18.1.linux-amd64.tar.gz
mkdir -p ~/go/{bin,src,pkg}
echo 'export GOROOT=/usr/local/go' >> ~/.profile
echo 'export PATH="$PATH:/usr/local/go/bin"' >> ~/.profile 
echo 'export GOPATH="$HOME/go"' >> ~/.profile
echo 'export GOBIN="$GOPATH/bin"' >> ~/.profile
. ~/.profile

mkdir -p ~/go/src/k8s.io
cd ~/go/src/k8s.io
git clone https://github.com/mike-moran-amd/kubernetes.git
cd kubernetes
git checkout uncore
cd hack
./install-etcd.sh
echo 'PATH=/root/go/src/k8s.io/kubernetes/third_party/etcd:${PATH}' >> ~/.bashrc
. ~/.bashrc

go install golang.org/x/tools/gopls@latest  # for MScode
./local-up-cluster.sh  # this takes a minute AND BLOCKS!
"""
