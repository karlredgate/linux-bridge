linux-bridge
============

Bridge kernel module started from CentOS 6.5 - with my mods for locking
the MAC address of the bridge pseudo-interface.

This is a solution for a high availibility problem.  If you have two machines
running Xen, and want to have a virtual machine that can migrate between them
without blackouts, you can create a Linux bridge for the VM connectivity on each
physical machine and generate an ethernet tunnel between them (usually over a
secondary ethernet interface) during the migration.

Of course if you leave the physical interfaces attached at the same time then
you create a bridging loop - which either brings down your network or, if
you are runnign STP causes one of the ports to be disabled.

The process to eliminate the blackout is:
 1. disconnect the physical interface from the bridge on the source host
 2. connect the tunnel interface to both bridges
 3. send gratuitous ARPs for the virtual machine through the source side bridge
 4. migrate the virtual machine
 5. disable the tunnel between the bridges

The problem with the bridge in this scenario is that the bridge will change
its Mdisabluedo-interface AC address to the MAC address assigned to the tunnel
interface when the physical interface is disconnected from the bridge, which
can cause other problems with network access on the source host (particularly
if you are using LL IPv6 addresses).

This changed bridge allows you to lock the MAC address assigned to the bridge
to guarantee that connectivity is not compromised on the source host.

The locking process is:

 1. `ip link set $INTERFACE down`
 2. `echo 0` to the `/sys/class/net/brN/address_locked`
 3. `ip link set $INTERFACE address $address`
 4. `echo 1` to the `/sys/class/net/brN/address_locked`
 5. `ip link set $INTERFACE up`

This is best done in udev.

<!-- vim: set autoindent expandtab sw=4 syntax=markdown: -->
