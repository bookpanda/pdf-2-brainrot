#!/bin/bash

# make them available to other processes (child processes) that are spawned by the current shell
export APP_NAME="${APP_NAME}"
export PORT="${PORT}"
export AWS_REGION="${AWS_REGION}"
export AWS_BUCKET_NAME="${AWS_BUCKET_NAME}"

sudo yum update -y
sudo yum install -y docker

sudo systemctl enable docker
sudo systemctl start docker

sudo docker pull ghcr.io/bookpanda/pdf-2-brainrot:latest

sudo docker run -d \
  -p ${PORT}:${PORT} \
  --name ${APP_NAME} \
  -e APP_NAME="${APP_NAME}" \
  -e PORT="${PORT}" \
  -e AWS_REGION="${AWS_REGION}" \
  -e AWS_BUCKET_NAME="${AWS_BUCKET_NAME}" \
  ghcr.io/bookpanda/pdf-2-brainrot:latest

cat <<EOF | sudo tee /etc/systemd/system/${APP_NAME}.service
[Unit]
Description=${APP_NAME}
After=network.target

[Service]
ExecStart=/usr/bin/docker start -a ${APP_NAME}
ExecStop=/usr/bin/docker stop ${APP_NAME}
Restart=always
User=ubuntu

[Install]
WantedBy=multi-user.target
EOF
echo "Systemd service created"

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable ${APP_NAME}
sudo systemctl start ${APP_NAME}
echo "Systemd service started"