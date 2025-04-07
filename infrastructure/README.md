# Commands
```bash
chmod 400 "pdf2br-key.pem"
ssh -i "pdf2br-key.pem" ec2-user@52.76.65.119


# clean key
ssh-keygen -R 54.251.110.185

# mark ec2 as tainted, will be recreated in apply (used for user_data changes)
terraform taint module.ec2.aws_instance.backend
```