
TOUCHED_PATHS = [
    "/usr/share/keyrings/docker-archive-keyring.gpg",
    "/etc/apt/sources.list.d/docker.list",
    "/usr/local/sbin/runc",
    "/etc/containerd/config.toml",  # SystemCgroup = true  #disabled_plugins
    "/etc/modules-load.d/k8s.conf",  # br_netfilter
    "/etc/sysctl.d/k8s.conf",  # net.bridge.bridge-nf-call-ip6tables = 1; net.bridge.bridge-nf-call-iptables = 1; net.ipv4.ip_forward = 1
    "/etc/fstab",  # comment out swap line
    "/etc/apt/sources.list.d/kubernetes.list",
    "$HOME/.kube/config",
    "/etc/containers/registries.conf",  # append unqualified-search-registries=["docker.io"]
]

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


class PersistentVolume:
    def __init__(self, **kwargs):
        kwargs = dict(kwargs)  # get our own shallow copy
        kwargs['kind'] = kwargs.get('kind') or 'StorageClass'
        kwargs['metadata'] = kwargs.get('metadata') or {}
        del_key_list = []
        for key, val in kwargs.items():
            if key.startswith('metadata_'):
                # move the "metadata_" prefixed keys to the metadata dict
                meta_key = key[len('metadata_'):]
                kwargs['metadata'][meta_key] = val
                # also delete the compound key in kwargs
                del_key_list.append(key)
        for key in del_key_list:
            del kwargs[key]
        # TODO parameters work like metadata...
        self.kwargs = kwargs

    @property
    def kind(self):
        return self.kwargs['kind']

    def to_yaml(self):
        yaml_lines = []
        for key, val in sorted(self.kwargs.items()):
            if key == 'metadata':
                # this is a dict
                yaml_lines.append('metadata:')
                for meta_key, meta_val in val.items():
                    yaml_lines.append(f'  {meta_key}: {meta_val}')
                pass
            else:
                yaml_lines.append(f'{key}: {val}')
        return '\n'.join(yaml_lines)


class LocalPersistentVolume(PersistentVolume):
    """
    Example from: https://kubernetes.io/docs/concepts/storage/storage-classes/#local
    >>> print(LocalPersistentVolume().to_yaml())
    apiVersion: storage.k8s.io/v1
    kind: StorageClass
    metadata:
      name: local-storage
    provisioner: kubernetes.io/no-provisioner
    volumeBindingMode: WaitForFirstConsumer
    """
    def __init__(self,
                 api_version="storage.k8s.io/v1",
                 # kind="StorageClass",  subsumed
                 metadata_name="local-storage",
                 provisioner="kubernetes.io/no-provisioner",
                 volume_binding_mode="WaitForFirstConsumer",  # delay volume binding until Pod scheduling
                 **kwargs):
        super(LocalPersistentVolume, self).__init__(
            apiVersion=api_version,
            metadata_name=metadata_name,
            provisioner=provisioner,
            volumeBindingMode=volume_binding_mode,
            **kwargs)
