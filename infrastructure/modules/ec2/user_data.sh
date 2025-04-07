#!/bin/bash

# make them available to other processes (child processes) that are spawned by the current shell
export APP_NAME="${APP_NAME}"
export PORT="${PORT}"
export AWS_REGION="${AWS_REGION}"
export AWS_BUCKET_NAME="${AWS_BUCKET_NAME}"
export GITHUB_REPO="${GITHUB_REPO}"

apt update -y
apt install -y git curl unzip python3-poetry python3-venv

cd /opt
git clone "${GITHUB_REPO}"
cd pdf-2-brainrot/backend
echo "GitHub repo cloned"

poetry install

mkdir -p /etc/${APP_NAME}
cat <<EOF > /etc/systemd/system/${APP_NAME}.service
[Unit]
Description=${APP_NAME}
After=network.target

[Service]
ExecStart=/usr/bin/poetry run python run.py
WorkingDirectory=/opt/pdf-2-brainrot/backend
Restart=always
EnvironmentFile=/etc/${APP_NAME}/env
User=ubuntu

[Install]
WantedBy=multi-user.target
EOF
echo "Systemd service created"

systemctl daemon-reexec
systemctl daemon-reload
systemctl enable ${APP_NAME}
systemctl start ${APP_NAME}
echo "Systemd service started"