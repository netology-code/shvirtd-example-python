#!/bin/bash

set -e

apt update
apt install -y git openssh-client curl


# 2. Установка Docker
echo "2. Установка Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh

# 3. Установка Docker Compose V2 (плагин)
echo "3. Установка Docker Compose..."
mkdir -p /root/.docker/cli-plugins
curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /root/.docker/cli-plugins/docker-compose
chmod +x /root/.docker/cli-plugins/docker-compose

# Проверка установки




eval "$(ssh-agent -s)"

if [ -f "./id_rsa" ]; then
    chmod 600 ./id_rsa 
    ssh-add ./id_rsa
else
    echo "Файл ./id_rsa не найден"
    exit 1
fi

ssh-keyscan -H github.com >> ~/.ssh/known_hosts 2>/dev/null

git clone git@github.com:alexmolov/shvirtd-example-python.git

cp ./.env  ./shvirtd-example-python/.env

cd shvirtd-example-python

docker compose up -d 

echo "Скрипт успешно выполнен"