#!/bin/bash

# Minecraft AI Cloud Setup Script
echo "🚀 Setting up Minecraft AI Cloud Environment..."

# Update and install system dependencies
sudo apt-get update
sudo apt-get install -y \
    python3-tk \
    python3-dev \
    xvfb \
    x11vnc \
    fluxbox \
    wget \
    curl \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Install Jupyter
pip install jupyter notebook

# Download pre-trained models
echo "📥 Downloading pre-trained models..."
mkdir -p models
cd models

# Download YOLO models (example URLs - replace with actual)
wget -O mob_detector.pt https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
wget -O block_detector.pt https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt

# Create desktop shortcut
echo "📝 Creating desktop configuration..."
cat > ~/Desktop/minecraft_ai.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Minecraft AI
Comment=Cloud Minecraft AI Player
Exec=python /workspaces/minecraft-cloud-ai/main.py
Icon=utilities-terminal
Terminal=true
Categories=Development;
EOF

chmod +x ~/Desktop/minecraft_ai.desktop

# Create VNC startup script
cat > /usr/local/bin/start-vnc.sh << 'EOF'
#!/bin/bash
# Start VNC server for remote desktop access
Xvfb :1 -screen 0 1024x768x24 &
export DISPLAY=:1
fluxbox &
x11vnc -display :1 -forever -usepw -rfbport 5900 -shared &
echo "VNC server started on port 5900"
echo "Connect with VNC viewer to: localhost:5900"
echo "Web VNC available at: http://localhost:6080/vnc.html"
EOF

chmod +x /usr/local/bin/start-vnc.sh

echo "✅ Setup complete!"
echo "📋 Next steps:"
echo "1. Run: start-vnc.sh"
echo "2. Connect via VNC to view the desktop"
echo "3. Run: python main.py"
