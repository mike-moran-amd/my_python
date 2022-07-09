#!/usr/bin/python
# encoding=UTF-8

UBUNTU_INSTALL_K8S_SCRIPT = '''
apt-get update
apt-get -y upgrade <<EOF
Y
EOF

curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list
apt update
apt -y install vim git curl wget kubelet kubeadm kubectl
apt-mark hold kubelet kubeadm kubectl
sudo swapoff -a
tee /etc/modules-load.d/containerd.conf <<EOF
overlay
br_netfilter
EOF

modprobe overlay
modprobe br_netfilter
tee /etc/sysctl.d/kubernetes.conf<<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

sysctl --system
apt install -y curl gnupg2 software-properties-common apt-transport-https ca-certificates
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt update
apt install -y containerd.io
mkdir -p /etc/containerd
containerd config default>/etc/containerd/config.toml
systemctl restart containerd
systemctl enable containerd
systemctl enable kubelet
kubeadm config images pull
kubeadm config images pull --cri-socket /run/containerd/containerd.sock
'''

UBUNTU_INSTALL_K8S_SCRIPT_MASTER = '''
kubeadm init --pod-network-cidr=192.168.0.0/16
'''

DOIT = """
apt-get update
apt-get -y upgrade <<EOF
Y
EOF

curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list
apt update
apt -y install vim git curl wget kubelet kubeadm kubectl
apt-mark hold kubelet kubeadm kubectl
swapoff -a
tee /etc/modules-load.d/containerd.conf <<EOF
overlay
br_netfilter
EOF

modprobe overlay
modprobe br_netfilter
tee /etc/sysctl.d/kubernetes.conf<<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

sysctl --system
apt install -y curl gnupg2 software-properties-common apt-transport-https ca-certificates
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt update
apt install -y docker-ce containerd.io
mkdir -p /etc/containerd
containerd config default>/etc/containerd/config.toml
systemctl restart containerd
systemctl enable containerd
systemctl enable kubelet
kubeadm config images pull
kubeadm config images pull --cri-socket /run/containerd/containerd.sock
"""

MASTER = """
kubeadm init --pod-network-cidr=192.168.0.0/16
# the bottom of the above command has a long multiline command to use on worker nodes 

IF NOT ROOT:
    mkdir -p $HOME/.kube
    cp -f /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config
ELSE:  # ROOT
    export KUBECONFIG=/etc/kubernetes/admin.conf
    
kubectl get nodes
kubectl get pods -o wide

# Install network plugin on Master
kubectl create -f https://docs.projectcalico.org/manifests/tigera-operator.yaml
kubectl create -f https://docs.projectcalico.org/manifests/custom-resources.yaml
kubectl get nodes -o wide

# Remove taint on the master node:
kubectl taint nodes --all node-role.kubernetes.io/master-

# Test Deploy
kubectl apply -f https://k8s.io/examples/pods/commands.yaml
# see completion
kubectl get pods -o wide
kubectl delete -f https://k8s.io/examples/pods/commands.yaml

# watch kubectl get pods --all-namespaces
"""

"""
mfm@u20044:~$ history
    1  #apt-get update
    2  sudo apt-get update
    3  sudo apt-get upgrade
    4  curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add
    5  echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
    6  sudo apt update
    7  sudo apt -y install vim git curl wget kubelet kubeadm kubectl
    8  sudo apt-mark hold kubelet kubeadm kubectl
    9  sudo swapoff -a
   10  sudo tee /etc/modules-load.d/containerd.conf <<EOF
overlay
br_netfilter
EOF

   11  sudo modprobe overlay
   12  sudo modprobe br_netfilter
   13  sudo tee /etc/sysctl.d/kubernetes.conf<<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

   14  sudo sysctl --system
   15  sudo apt install -y curl gnupg2 software-properties-common apt-transport-https ca-certificates
   16  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
   17  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
   18  sudo apt update
   19  sudo apt install -y containerd.io
   20  sudo mkdir -p /etc/containerd
   21  containerd config default
   22  containerd config default | sudo tee /etc/containerd/config.toml
   23  ll /etc/containerd
   24  sudo systemctl restart containerd
   25  sudo systemctl enable containerd
   26  sudo systemctl enable kubelet
   27  sudo kubeadm config images pull
   28  echo $HOME
   29  sudo systemctl status docker
   30  which docker
   31  which docker_ce
   32  sudo apt-cache policy docker-ce
   33  sudo apt install docker_ce
   34  sudo apt install docker-ce
   35  sudo systemctl status docker
   36  docker
   37  groups
   38  sudo usermod -aG docker $(USER)
   39  sudo usermod -aG docker mfm
   40  su - mfm
   41  history
   42  docker
   43  which docker
   44  ll /usr/bin
   45  ll /usr/bin docker
   46  ll /usr/bin/docker
   47  history
"""

"""
root@mm1:~/go/src/k8s.io/kubernetes/hack# history
    1  vi doit
    2  sh doit
    3  vi doit2
    4  sh doit2
    5  curl -LO https://golang.org/dl/go1.18.1.linux-amd64.tar.gz
    6  ll
    7  tar -C /usr/local -xvzf go1.18.1.linux-amd64.tar.gz
    8  ll
    9  go env GOPATH
   10  which go
   11  exit
   12  whic go
   13  go
   14  which go
   15  cd /usr/local
   16  ll
   17  cd go
   18  ll
   19  export GOROOT=`pwd`
   20  echo $GOROOT
   21  which go
   22  echo $PATH
   23  cd
   24  ll
   25  pwd
   26  mkdir go
   27  cd go
   28  mkdir -p ~/go_projects/{bin,src,pkg}
   29  ll
   30  mkdir -p ~/go/{bin,src,pkg}
   31  ll
   32  pwd
   33  cd ..
   34  ll
   35  cd ..
   36  ls
   37  cd go
   38  cd
   39  cd go
   40  cd go[
   41  cd go
   42  pwd
   43  ll
   44  mkdir -p ~/go_projects/{bin,src,pkg}
   45  export  PATH=$PATH:/usr/local/go/bin
   46  go version
   47  echo $GOPATH
   48  cd
   49  cd
   50  ll
   51  vi .profile
   52  export PATH=$PATH:/usr/local/go/bin
   53  export GOPATH="$HOME/go"
   54  export GOBIN="$GOPATH/bin"
   55  source ~/.profile
   56  echo $GOPATH
   57  echo $GOBIN
   58  echo $GOROOT
   59  go version
   60  cd go
   61  ls
   62  cd src
   63  ls
   64  mkdir k8s.io
   65  cd k8s.io/
   66  git clone https://github.com/kubernetes/kubernetes/git
   67  git clone https://github.com/kubernetes/kubernetes.git
   68  ll
   69  cd kubernetes/
   70  ll
   71  history
   72  ll
   73  ll hack/
   74  cd hack
   75  ls
   76  ./install-etcd.sh
   77  vi ~/.profile
   78  ll
   79  ll ~
   80  vi ~/.bashrc
   81  export PATH="/root/go/src/k8s.io/kubernetes/third_party/etcd:${PATH}"
   82  echo $PATH
   83  etcd
   84  vi ~/doit3
   85  sh ~/doit3
   86  cd ..
   87  cd hack/
   88  ll
   89  ll l*
   90  ./local-up-cluster.sh
   91  apt-get install build-essential
   92  ./local-up-cluster.sh
   93  bg
   94  history
   95  ps -a
   96  history
   
root@mm1:~/go/src/k8s.io/kubernetes# history
    1  vi doit
    2  sh doit
    3  vi doit2
    4  sh doit2
    5  curl -LO https://golang.org/dl/go1.18.1.linux-amd64.tar.gz
    6  ll
    7  tar -C /usr/local -xvzf go1.18.1.linux-amd64.tar.gz
    8  ll
    9  go env GOPATH
   10  which go
   11  exit
   12  cd go
   13  cd ssrc
   14  cdsrc
   15  cd srwc
   16  cd src
   17  ls
   18  cd k8s.io/
   19  ls
   20  cd kubernetes/
   21  ll
   22  export KUBECONFIG=/var/run/kubernetes/admin.kubeconfig
   23  cluster/kubectl.sh
   24  cluster/kubectl.sh get nodes
   25  history
   
root@mm1:~# cat doit*
apt-get update
apt-get -y upgrade <<EOF
Y
EOF

apt install -y curl gnupg2 software-properties-common apt-transport-https ca-certificates
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt update
apt install -y docker-ce

apt install -y containerd.io
mkdir -p /etc/containerd
containerd config default>/etc/containerd/config.toml
systemctl restart containerd
systemctl enable containerd

# run this on the remote host
go install -v golang.org/x/tools/gopls@latest

The VSC IDE needed to install these to make the debug unit tests available...
Installing github.com/ramya-rao-a/go-outline@latest (/root/go/bin/go-outline) SUCCEEDED
Installing github.com/go-delve/delve/cmd/dlv@latest (/root/go/bin/dlv) SUCCEEDED
Installing honnef.co/go/tools/cmd/staticcheck@latest (/root/go/bin/staticcheck) SUCCEEDED
Installing golang.org/x/tools/gopls@latest (/root/go/bin/gopls) SUCCEEDED
"""

"""
https://www.tecmint.com/install-go-in-linux/
https://code.visualstudio.com/docs/?dv=win
https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack
https://console.equinix.com/projects/c299cb5b-9fb7-41da-8f16-c65fff2fbace
https://visualstudio.microsoft.com/
https://github.com/kubernetes/community/blob/master/contributors/guide/github-workflow.md
https://github.com/golang/go/wiki/SettingGOPATH#windows
https://marketplace.visualstudio.com/items?itemName=golang.go
https://code.visualstudio.com/docs/editor/debugging
https://stackoverflow.com/questions/17480044/how-to-install-the-current-version-of-go-in-ubuntu-precise
https://docs.microsoft.com/en-us/windows/wsl/install
"""

"""
root@mm2:~/go_projects/src/k8s.io/kubernetes# cluster/kubectl.sh get nodes
NAME        STATUS   ROLES    AGE   VERSION
127.0.0.1   Ready    <none>   87m   v1.24.0-beta.0.137+a750d8054a6cb3
root@mm2:~/go_projects/src/k8s.io/kubernetes# history
    1  uname -a
    2  apt-get update
    3  apt-get -y upgrade <<EOF
Y
EOF

    4  apt install -y curl gnupg2 software-properties-common apt-transport-https ca-certificates
    5  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
    6  add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    7  apt update
    8  apt install -y docker-ce
    9  curl -LO https://golang.org/dl/go1.18.1.linux-amd64.tar.gz
   10  tar -C /usr/local -xvzf go1.18.1.linux-amd64.tar.gz
   11  export GOROOT=/usr/local/go
   12  echo $GOROOT
   13  which go
   14  export  PATH=$PATH:/usr/local/go/bin
   15  which go
   16  go version
   17  mkdir -p ~/go_projects/{bin,src,pkg}
   18  pwd
   19  ll
   20  ll go_projects/
   21  history
   22  export GOPATH="$HOME/go"
   23  export GOBIN="$GOPATH/bin"
   24  echo $GOPATH
   25  echo $GOBIN
   26  echo $GOROOT
   27  export GOPATH="$HOME/go_projects"
   28  export GOBIN="$GOPATH/bin"
   29  echo $GOPATH
   30  echo $GOBIN
   31  echo $GOROOT
   32  mkdir -p ~/go_projects/src/k8s.io
   33  cd ~/go_projects/src/k8s.io
   34  git clone https://github.com/kubernetes/kubernetes.git
   35  cd kubernetes/
   36  cd hack/
   37  ./install-etcd.sh 
   38  export PATH="/root/go/src/k8s.io/kubernetes/third_party/etcd:${PATH}"
   39  apt install -y containerd.io
   40  mkdir -p /etc/containerd
   41  containerd config default>/etc/containerd/config.toml
   42  systemctl restart containerd
   43  systemctl enable containerd
   44  apt-get install build-essential
   45  ./local-up-cluster.sh
   46  history
   47  echo $PATH
   48  etcd
   49  export PATH=/root/go_projects/src/k8s.io/kubernetes/third_party/etcd:/root/.vscode-server/bin/dfd34e8260c270da74b5c2d86d61aee4b6d56977/bin/remote-cli:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/local/go/bin
   50  ./local-up-cluster.sh
   51  bg
   52  export KUBECONFIG=/var/run/kubernetes/admin.kubeconfig
   53  jobs
   54  bg
   55  cluster/kubectl.sh
   56  cd ..
   57  cluster/kubectl.sh
   58  cluster/kubectl.sh get nodes
   59  history
"""

"""
#220416:
root@mm0:~/go/src/k8s.io/kubernetes/hack# history
    1  uname -a
    2  vi doit12
    3  sh doit12
    4  curl -LO https://golang.org/dl/go1.18.1.linux-amd64.tar.gz
    5  tar -C /usr/local -xvzf go1.18.1.linux-amd64.tar.gz
    6  cd /usr/local/go
    7  export GOROOT=`pwd`
    8  echo $GOROOT
    9  which go
   10  cd
   11  pwd
   12  mkdir go
   13  cd go
   14  mkdir -p ~/go/{bin,src,pkg}
   15  ll
   16  export  PATH=$PATH:/usr/local/go/bin
   17  go version
   18  vi ~/.profile
   19  export GOPATH="$HOME/go"
   20  export GOBIN="$GOPATH/bin"
   21  echo $GOPATH
   22  echo $GOBIN
   23  echo $GOROOT
   24  cd src
   25  mkdir k8s.io
   26  cd k8s.io/
   27  git clone https://github.com/kubernetes/kubernetes.git
   28  cd kubernetes/
   29  cd hack
   30  ./install-etcd.sh
   31  vi ~/.bashrc
   32  echo $PATH
   33  source ~/.bashrc
   34  echo $PATH
   35  etcd
   36  vi ~/doit3
   37  sh ~/doit3
   38  apt-get install build-essential
   39  history
   
root@mm0:~/go/src/k8s.io/kubernetes# history
    1  export KUBECONFIG=/var/run/kubernetes/admin.kubeconfig
    2  cd go/src/k8s.io/kubernetes/
    3  cluster/kubectl.sh
    4  cluster/kubectl.sh get nodes
    5  history
    6  go install -v golang.org/x/tools/gopls@latest
    
    ## AFTER THIS, you need to enable the remote extension from MSC 
    # on far left tab (Extensions), you should see GO "Rich Language Support ..." click install

    7  history
"""

ALL_BUT_K8S = """
apt-get update
apt-get -y upgrade <<EOF
Y
EOF

apt install -y build-essential curl gnupg2 software-properties-common apt-transport-https ca-certificates
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt update
apt install -y docker-ce containerd.io
mkdir -p /etc/containerd
containerd config default>/etc/containerd/config.toml
systemctl restart containerd
systemctl enable containerd

"""


"""
root@mm2:~/go/src# history
    1  uname -a
    2  apt-get update
    3  apt-get -y upgrade <<EOF
Y
EOF

    6  apt install -y build-essential curl gnupg2 software-properties-common apt-transport-https ca-certificates
    7  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
    8  add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    9  apt update
   10  apt install -y docker-ce containerd.io
   11  mkdir -p /etc/containerd
   12  containerd config default>/etc/containerd/config.toml
   13  systemctl restart containerd
   14  systemctl enable containerd
   15  curl -LO https://golang.org/dl/go1.18.1.linux-amd64.tar.gz
   16  tar -C /usr/local -xvzf go1.18.1.linux-amd64.tar.gz
   17  cd /usr/local/go
   18  export GOROOT=`pwd`
   19  cd
   20  mkdir go
   21  cd go
   22  mkdir -p ~/go/{bin,src,pkg}
   23  export PATH=$PATH:/usr/local/go/bin
   24  go version
   25  go install -v golang.org/x/tools/gopls@latest
   26  vi ~/.profile
   27  source ~/.profile
   28  cat ~/.profile
   29  echo $GOPATH
   30  echo $GOBIN
   31  $GOROOT
   32  echo $GOROOT
   33  mkdir -p src/k8s.io
   34  cd src/k8s.io
   35  git clone https://github.com/kubernetes/kubernetes.git
   36  cd kubernetes/hack/
   37  ./install-etcd.sh
   38  vi ~/.bashrc # ADD export PATH="/root/go/src/k8s.io/kubernetes/third_party/etcd:${PATH}"
   39  source ~/.bashrc
   40  echo $PATH
   41  ./local-up-cluster.sh &
   42  jobs
   43  export KUBECONFIG=/var/run/kubernetes/admin.kubeconfig
   44  cd ~/go/src/k8s.io/kubernetes/
   45  cluster/kubectl.sh get nodes
   46  history
root@mm2:~/go/src# 
"""

NEW_DOIT = """
uname -a
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
cd kubernetes/hack/
./install-etcd.sh
echo 'PATH=/root/go/src/k8s.io/kubernetes/third_party/etcd:${PATH}' >> ~/.bashrc
. ~/.bashrc

go install golang.org/x/tools/gopls@latest  # for MScode
./local-up-cluster.sh &  # this takes a minute or two AND WOULD BLOCK!

### TO USE IN ANOTHER WINDOW (If blocked)
# export KUBECONFIG=/var/run/kubernetes/admin.kubeconfig
# ~/go/src/k8s.io/kubernetes/cluster/kubectl.sh get nodes
"""

"""
#2204181700:  Instructions to enable Microsoft Studio Code 2022 Remote Debugging
    # This link has lots of info to get started, you will need to "Download and Install remote tools" (link)
    https://docs.microsoft.com/en-us/visualstudio/debugger/remote-debugging?view=vs-2022
   
   # I also installed WSL2, but you probably do not need it.
   https://docs.microsoft.com/en-us/windows/wsl/install
   # WARNING: THIS WILL BREAK YOUR VIRTUAl BOX 


#2204190945:  Step by step
    Go to Equinix Servers page: https://console.equinix.com/projects/c299cb5b-9fb7-41da-8f16-c65fff2fbace
    Click "New Server" button
    Select "ON DEMAND"
    Select Location (Dallas), c3.medium.x86 (EPYC 7402P 24-Core, OS (Ubuntu 20.04 LTS)
    Enter host name (mm10) and press "Deploy Now"
    It takes about two minutes for it to be provisioned... Copy IPV4 Address of box 147.75.55.105
    Open a cmd.exe window
    ssh -o StrictHostKeyChecking=no root@147.75.55.105
        $ vi new_doit  # cut-n-paste NEW_DOIT shell script above into editor and save ":wq"
        $ . new_doit  # this takes about 7 minutes to run
        $ jobs  # should show one running ./local-up-cluster.sh &
        $ export KUBECONFIG=/var/run/kubernetes/admin.kubeconfig
        $ cd ..  # kubernetes
        $ cluster/kubectl.sh get nodes # should show one node
        
    Microsoft Visual Studio Code uses a config file in your laptop .ssh directory  (Users/mikmoran/.ssh/config)
    Add a section to the config (e.g.):
        Host mm10
          HostName 147.75.55.105
          StrictHostKeyChecking no
          User root
    Click "File", "save"
    Click (green box bottom left IDE)
    Select "Connect to Host"
    Select the config we added earlier
    Select Linux
    Click "Extentions" icon in left side tabs, there should be Remote Containers, SSH, WSL, Remote Dev
    Type "go" in the "Search Extensions in Marketplace"
    A dim item "go" will have a button "Install in SSH: mm10", click it.
    Click the IDE navigation Explorer tab on left side tab pane
    Click "Open Folder"
        Select "go"
        Select "src"
        Press "OK"
    Navigate down to test file:
        # you will be prompted if you trust the authors of the files here, I said yes
        go/src/k8s.io/kubernetes/pkg/kublet/cm/cpumanager/cpu_assignment_test.go
        # You will get a WARNING on bottom right status bar the Analysis Tools Missing
            Click on the warning and select "Install", it will say you are Ready to go
        Almost ...
        In the Details, navigate to line number 116 and put a breakpoint (click just left of number)
        Go back up to line 28, above the line there is a "debug test" button, click it
        The debugger should be paused at your breakpoint and shows Variables panel.
    Happy Programming!
        
        
        
        
        
    
    
"""