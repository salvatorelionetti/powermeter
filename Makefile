install: /lib/systemd/system/powermeter.service
	sudo apt-get install --assume-yes libmodbus-dev

/lib/systemd/system/powermeter.service: powermeter.service powermeter.out
	sudo cp powermeter.service /lib/systemd/system
	# First time also start the service at startup
	sudo systemctl enable powermeter.service

powermeter.out: powermeter.c
	gcc -lmodbus $^ -o $@

.PHONY: install
