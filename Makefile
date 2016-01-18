install: /lib/systemd/system/powermeter.service
	sudo apt-get install --assume-yes libmodbus-dev

/lib/systemd/system/powermeter.service: powermeter.service
	sudo cp powermeter.service /lib/systemd/system
	# First time also start the service at startup
	sudo systemctl enable powermeter.service

.PHONY: install
