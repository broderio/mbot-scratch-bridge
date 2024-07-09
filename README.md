# Instructions for Running MBot-Scratch

### 1. Clone other repositories
```bash
git clone https://github.com/broderio/mbot-scratch-gui
git clone https://github.com/broderio/mbot-scratch-vm
```

### 2. Setup Scratch Virtual Machine
```bash
cd mbot-scratch-vm
npm install
sudo npm link
```

### 3. Setup Scratch GUI
```bash
cd ../mbot-scratch-gui
npm install
npm link scratch-vm
npm start
```

### 4. Start backend (in a separate terminal)
```bash
cd ../mbot-scratch-bridge
python3 serverTest.py
```