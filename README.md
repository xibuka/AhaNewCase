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

  the usage of the arguments are:
  --toAddr      the email address where the notice should be send to.
  --fromAddr    send from email address. Must be a gmail address
  --fromAddrPW  password of the send from email address.
  --rhuser      RH account to access unified.gsslab.rdu2.redhat.com
  --rhpass      password for RH account

  Note: FromAddr email need to be a Gmail account.

# Todo List
- [ ] make this tool to an web service to folks
- [ ] user can add/remove themself to the service with email address
- [ ] user can change their subscribed SBR plate
- [ ] when NCQ comes up, send mail to all users who has subscibed this SBR
- [ ] send NCQ case only opened in APAC business hours.
- [ ] analyze FTS table, address the policy of how to sending FTS case.
