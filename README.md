# Exploring-new-long-lived-particles-at-the-LHC-topological-signatures-by-charge-and-lifetime.
# Exploring-new-long-lived-particles-at-the-LHC-topological-signatures-by-charge-and-lifetime.
# Exploring-new-long-lived-particles-at-the-LHC-topological-signatures-by-charge-and-lifetime.
# Read more about SSH config files: https://linux.die.net/man/5/ssh_config
Host sbgli2.in2p3.fr
    HostName sbgli2.in2p3.fr
    User xmadre
    ProxyCommand ssh xmadre@sbgli2.in2p3.fr -W %h:%p
    ProxyCommand cd /opt/sbg/cms/safe1/cms/xmadre/ 
