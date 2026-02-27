#!/bin/bash
# Деплой продающего Telegram-бота RecPlace на Timeweb
# Запуск: bash deploy_sales_bot.sh

set -e

# ==================== НАСТРОЙКИ ====================
SERVER="77.232.128.173"
SERVER_PASS="dRg-34pW@WC_yH"
BOT_DIR="/opt/sales_bot"
BOT_NAME="recplace_sales_bot"
# ===================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err() { echo -e "${RED}[✗]${NC} $1"; exit 1; }

# Проверяем sshpass
if ! command -v sshpass &>/dev/null; then
    warn "sshpass не установлен. Устанавливаю через Homebrew..."
    brew install sshpass || err "Не удалось установить sshpass. Установите вручную: brew install sshpass"
fi

# Ищем файлы бота рядом со скриптом
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
log "Папка скрипта: $SCRIPT_DIR"

# Проверяем наличие .env
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    err "Файл .env не найден в $SCRIPT_DIR\nСоздайте его по примеру .env.example"
fi

# SSH-алиас для удобства
SSH="sshpass -p '$SERVER_PASS' ssh -o StrictHostKeyChecking=no root@$SERVER"
SCP="sshpass -p '$SERVER_PASS' scp -o StrictHostKeyChecking=no"

log "Подключаюсь к серверу $SERVER..."
eval $SSH "echo 'Подключение успешно'" || err "Не удалось подключиться к серверу"

log "Создаю директорию $BOT_DIR на сервере..."
eval $SSH "mkdir -p $BOT_DIR"

log "Копирую файлы на сервер..."
eval $SCP \
    "$SCRIPT_DIR/main.py" \
    "$SCRIPT_DIR/handlers.py" \
    "$SCRIPT_DIR/admin.py" \
    "$SCRIPT_DIR/keyboards.py" \
    "$SCRIPT_DIR/states.py" \
    "$SCRIPT_DIR/texts.py" \
    "$SCRIPT_DIR/database.py" \
    "$SCRIPT_DIR/config.py" \
    "$SCRIPT_DIR/bitrix.py" \
    "$SCRIPT_DIR/requirements.txt" \
    "$SCRIPT_DIR/.env" \
    "root@$SERVER:$BOT_DIR/"

log "Устанавливаю Python и зависимости..."
eval $SSH "
    apt-get update -qq &&
    apt-get install -y -qq python3 python3-pip python3-venv &&
    cd $BOT_DIR &&
    python3 -m venv venv &&
    ./venv/bin/pip install -q --upgrade pip &&
    ./venv/bin/pip install -q -r requirements.txt
"

log "Создаю systemd-сервис..."
eval $SSH "cat > /etc/systemd/system/${BOT_NAME}.service << 'SERVICEEOF'
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
SERVICEEOF"

log "Запускаю бота как системный сервис..."
eval $SSH "
    systemctl daemon-reload &&
    systemctl enable ${BOT_NAME} &&
    systemctl restart ${BOT_NAME}
"

sleep 3

log "Проверяю статус..."
eval $SSH "systemctl status ${BOT_NAME} --no-pager | head -20"

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}  Бот успешно задеплоен!        ${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Полезные команды (выполнять на сервере):"
echo "  Логи:    journalctl -u ${BOT_NAME} -f"
echo "  Статус:  systemctl status ${BOT_NAME}"
echo "  Стоп:    systemctl stop ${BOT_NAME}"
echo "  Рестарт: systemctl restart ${BOT_NAME}"
