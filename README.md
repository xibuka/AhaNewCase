Inform you by sending email when you have new case in Cloud Prods & Envs,Stack,Ceph,Gluster,CFME

# Usage:

0. install docker 
```
# yum install -y docker
```

1. pull the docker images.

```
# docker pull wenhan/ahanewcase
```

2. run the container

```
# docker run -d --privileged wenhan/ahanewcase:latest
<container ID>
```

3. login to the container and get subscribed by mail and SBR
```
# docker exec -ti <container ID> /bin/sh
sh-4.4# ./register.py --name=<NAME> --mail=<MAIL> --sbr=<SBR> --action=add
```

action can also be remove and show

```
sh-4.4# ./register.py --name=<NAME> --mail=<MAIL> --sbr=<SBR> --action=remove
sh-4.4# ./register.py --name=<NAME> --mail=<MAIL> --sbr=<SBR> --action=show
```

4. initialize the info used for send mail

```
sh-4.4# ./initConfig.py --fromAddr=<YourAccount@gmail.com>   \
                        --fromAddrPW=<YourGmailPassword>     \
                        --rhuser=<rhn-UserName>              \
                        --rhpass=<rhn-Password>
```

The usage of the arguments are:

```
arguments:
  -h, --help            show this help message and exit
  --fromAddr FROMADDR   send from email address. must be a gmail account
  --fromAddrPW FROMADDRPW
                        password of the send from email address.
  --rhuser RHUSER       RH account to access unified web site
  --rhpass RHPASS       password for RH account

```

# Todo List
- [ ] make this tool to an web service to folks
- [x] user can add/remove themself to the service with email address
- [x] user can change their subscribed SBR plate
- [x] when NCQ comes up, send mail to all users who has subscibed this SBR
- [ ] send NCQ case only opened in APAC business hours.
- [x] analyze FTS table, address the policy of how to sending FTS case.
