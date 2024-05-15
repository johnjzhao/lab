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

```Build & run cpp solutions

Enterprise Virtual Encrypted Domain
Software (SVCI) Copyright (c) 1999-2024
              --- by SUNVALLEY COMPUTER INC.
 _                      _
| |_ ___ _ __ _ __ ___ (_)_ __  _____   ___ __
| __/ _ \ '__| '_ ` _ \| | '_ \/ __\ \ / / '__|
| ||  __/ |  | | | | | | | | | \__ \\ V /| |
 \__\___|_|  |_| |_| |_|_|_| |_|___/ \_/ |_|


Last login: Tue May 14 18:48:37 2024 from 192.168.75.172
itsupp@terminsvr:~$ cd lab
itsupp@terminsvr:~/lab$ mysol
Binary Tree Map:
       8
      / \
     /   \
    /     \
   5      10
  / \     / \
 2   6   9  11

itsupp@terminsvr:~/lab$
