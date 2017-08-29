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
# docker run -d wenhan/ahanewcase:latest          \
             --toAddr=<ToYou@domain.com>          \
             --fromAddr=<YourAccount@gmail.com>   \
             --fromAddrPW=<YourGmailPassword>     \
             --rhuser=<rhn-UserName>              \
             --rhpass=<rhn-Password>
```

The usage of the arguments are:

```
arguments:
  -h, --help            show this help message and exit
  --toAddr TOADDR       the email address where the notice should be send to.
  --fromAddr FROMADDR   send from email address. must be a gmail account
  --fromAddrPW FROMADDRPW
                        password of the send from email address.
  --rhuser RHUSER       RH account to access unified web site
  --rhpass RHPASS       password for RH account

```

# Todo List
- [ ] make this tool to an web service to folks
- [ ] user can add/remove themself to the service with email address
- [ ] user can change their subscribed SBR plate
- [ ] when NCQ comes up, send mail to all users who has subscibed this SBR
- [ ] send NCQ case only opened in APAC business hours.
- [ ] analyze FTS table, address the policy of how to sending FTS case.
