# Commands
```bash
chmod 400 "pdf2br-key.pem"
ssh -i "pdf2br-key.pem" ec2-user@13.251.24.12


# clean key
ssh-keygen -R 13.251.24.12

# mark ec2 as tainted, will be recreated in apply (used for user_data changes)
terraform taint module.ec2.aws_instance.backend

# check user_data progress on ec2
sudo tail -f /var/log/cloud-init-output.log

sudo docker run -p 8000:8000 --name "test" ghcr.io/bookpanda/pdf-2-brainrot:latest
docker run -p 8000:8000 --name "test" my-app

```