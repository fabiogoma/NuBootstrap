# NuProvisionerServer

### Sequence usage to build the API server from scratch:
```shellscript
$ cd /home/fabiom/vms/aws/bootstrap
$ python nu_iam_create.py
$ python nu_sqs_create.py
$ python nu_ec2_sg_create.py
$ python nu_s3_create.py
$ python nu_opsworks_create.py
```

### Sequence usage do destroy everything created before:
```shellscript
$ cd /home/fabiom/vms/aws/bootstrap
$ python nu_opsworks_delete.py
$ python nu_s3_delete.py
$ python nu_ec2_sg_delete.py
$ python nu_sqs_delete.py
$ python nu_iam_delete.py
```

### Schedule a new spot instance
```
curl -H "Content-Type: application/json" -X POST -d @/home/fabiom/vms/aws/helpers/schedule.json http://INSTANCE-IP/schedule/
```
### List spot instance requests
```
curl http://INSTANCE-IP/list/ | jq
```
### Check the status from one specific schedule
```
curl http://INSTANCE-IP/status/RANDOM-ID | jq
```
### Terminate the one specific schedule
```
curl http://INSTANCE-IP/callback/RANDOM-ID | jq
```