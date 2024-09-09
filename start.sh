sudo ifconfig lo multicast
sudo route add -net 224.0.0.0 netmask 224.0.0.0 dev lo
/usr/bin/python3 /home/mbot/scratch/mbot-scratch-bridge/scratchBridge.py
