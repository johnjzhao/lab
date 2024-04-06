## Quickstart
## Docker version 24.0.5
## Docker Compose version v2.2.3

To get CPP compiler & Python 3 up and running on docker container  run the following commands.
docker plugin install vieux/sshfs
```bash
git clone https://github.com/johnjzhao/lab.git
cd lab/Docker/
docker-compose build
docker-compose up -d

ssh -p 2222 itsupp@localhost

