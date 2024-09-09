#!/bin/bash
set -e  # Quit on error

if [ ! -f "/etc/systemd/system/mbot-scratch-bridge.service" ]; then
  # This is the first time installing.
  sudo cp mbot-scratch-bridge.service /etc/systemd/system/

  echo "Enabling MBot Scratch GUI  service."
  # Reload the service.
  sudo systemctl daemon-reload
  sudo systemctl enable mbot-scratch-bridge.service
  sudo systemctl start mbot-scratch-bridge.service
else
  # This service has already been installed. Pull new changes then restart it.
  sudo cp mbot-scratch-bridge.service /etc/systemd/system/
  # Fill in the path to this env.
  echo "MBot Scratch GUI  service is already enabled. Restarting it."
  sudo systemctl daemon-reload
  sudo systemctl restart mbot-scratch-bridge.service
fi

echo
echo "Done! The MBot Scratch Bridge is now running!"
