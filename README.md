# powermeter

Linux userspace code to export some Power Meter measurements over the Web.

Supported environment:

SW:
* Linux * (with systemd)
* libmodbus-dev package
* ThingSpeak account

HW:
* ABB B21 power meter 
* RS485 <-> USB converter
* A host machine with USB, e.g. PC, Raspberry PI.

To install, after downloaded the code: (systemd required)
```
make
```
