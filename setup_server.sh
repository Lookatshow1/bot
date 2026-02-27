#!/bin/bash
# Запускается ПРЯМО НА СЕРВЕРЕ
# Использование: curl -s <url> | bash
# или: bash setup_server.sh

BOT_DIR="/opt/sales_bot"
BOT_NAME="recplace_sales_bot"

set -e

echo "[1/5] Обновление системы..."
apt-get update -qq
apt-get install -y -qq python3 python3-pip python3-venv

echo "[2/5] Создание директории..."
mkdir -p $BOT_DIR
cd $BOT_DIR

echo "[3/5] Создание виртуального окружения..."
python3 -m venv venv
./venv/bin/pip install -q --upgrade pip

echo "[4/5] Установка зависимостей..."
./venv/bin/pip install -q aiogram==3.4.1 aiosqlite==0.19.0 aiohttp==3.9.1 python-dotenv==1.0.0

echo "[5/5] Создание systemd-сервиса..."
cat > /etc/systemd/system/${BOT_NAME}.service << EOF
[Unit]
Description=RecPlace Sales Bot
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=$BOT_DIR
ExecStart=$BOT_DIR/venv/bin/python main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable ${BOT_NAME}

echo ""
echo "Сервер готов! Теперь загрузи файлы в $BOT_DIR и запусти:"
echo "  systemctl start ${BOT_NAME}"
echo "  journalctl -u ${BOT_NAME} -f"
