# powermeter

Linux userspace code to export some Power Meter measurements over the Web.

Supported environment:

SW:
* Linux * (with systemd)
* libmodbus-dev package
* ThingSpeak account

HW:
* ABB B21 power meter 
* RS485 <-> USB converter (FTDI)

Indentify the name of the connected device with dmesg (or similar), e.g. /dev/ttyUSBx

Identify the major/minor number with lsusb (or similar), e.g. 0403:6001.

Identify the serial number of your USB converter with:
```
udevadm info -a -p  $(udevadm info -q path -n /dev/ttyUSBx) | grep serial
```

Then add an udev rule into file /etc/udev/rules.d/99-usb-serial-yourname.rules:
```
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", ATTRS{serial}=="A704FNG9", SYMLINK+="pm.serial"
```
by inserting yours major,minor,serial usb parameters.

Download in folder:
```
/home/pi/projects/powermeter
```

and install (systemd required) with
```
make
```

Note: By using bigger names for power meter serial device, e.g. '/dev/powermeter.serial', with libmodbus-dev 3.0.6-1 you got the following error:

```
The device string has been truncated
```

This is fixed into v3.1x
