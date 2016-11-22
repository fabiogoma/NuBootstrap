# NuProvisionerServer

### Sequence usage to build the API server from scratch:
```shellscript
$ cd /home/fabiom/vms/aws/bootstrap
$ python nu_iam_create.py
$ python nu_s3_create.py
$ python nu_sqs_create.py
$ python nu_ec2_sg_create.py
$ python nu_opsworks_create.py
```

### Sequence usage do destroy everything created before:
```shellscript
$ cd /home/fabiom/vms/aws/bootstrap
$ python nu_opsworks_delete.py
$ python nu_ec2_sg_delete.py
$ python nu_sqs_delete.py
$ python nu_s3_delete.py
$ python nu_iam_delete.py
```

### Schedule a new spot instance
```
curl -H "Content-Type: application/json" -X POST -d @/home/fabiom/vms/aws/helpers/schedule.json   
```
### List spot instance requests
```
curl http://35.164.34.142/list/ | jq
```