#!/bin/bash
sudo cp /home/hp/gps_logger/first_time_setup/gps-logging.service /etc/systemd/system/
systemctl daemon-reload
sudo systemctl enable gps-logging
