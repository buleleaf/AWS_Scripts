#cloud-config

packages:
  - python
  - python-pip
  - aws-cli
  - unzip
  - wget

write_files:
  - path: /tmp/tempcloudwatch/config.json
    content: |
      {
      "metrics": {
        "append_dimensions":{
            "InstanceId":"${aws:InstanceId}"
        },
        "aggregation_dimensions": [
            ["InstanceId"],
            ["AutoScalingGroupName"],
        ],
        "metrics_collected": {
        "mem": {
            "measurement": [
            "mem_used_percent"
            ],
            "metrics_collection_interval": 60
        }
        }
      }
      }
  - path: /usr/bin/rename_instance.py
    content: |
      #!/usr/bin/python

      import boto.ec2
      import boto3
      import requests
      import random
      import time
      import subprocess
      import json
      import os

      def create_record(name, record_type, target, zone, client):
        client.change_resource_record_sets(
          HostedZoneId=zone,
          ChangeBatch={
              'Changes': [
                  {
                      'Action': 'UPSERT',
                      'ResourceRecordSet': {
                          'Name': name,
                          'Type': record_type,
                          'TTL': 60,
                          'ResourceRecords': [
                              {
                                  'Value': target
                              },
                          ]
                      }
                  },
              ]
          }
        )


      time.sleep(random.randrange(5, 30))

      instance_data = json.loads((requests.get("http://169.254.169.254/latest/dynamic/instance-identity/document")).content)

      conn = boto.ec2.connect_to_region(instance_data['region'])
      r53 = boto3.client('route53', instance_data['region'])
      priv_ip = instance_data['privateIp']
      currentReservation = conn.get_all_instances(instance_ids=instance_data['instanceId'])
      currentInstance = [i for r in currentReservation for i in r.instances]
      for inst in currentInstance:
          instApp = inst.tags['Application']
          instType = inst.tags['csNomadClass']
          instEnvironment = inst.tags['Environment']

      count = 0
      instances = {}

      allReservations = conn.get_all_instances()
      for res in allReservations:
          for inst in res.instances:
              if 'csNomadClass' in inst.tags:
                  if inst.tags['csNomadClass'] == instType and \
                    inst.tags['Environment'] == instEnvironment and \
                    inst.state == 'running':
                      instances[inst.id] = inst.tags['Name']
                      count += 1

      for x in range(1, count + 1):
          name = instEnvironment + "-" + instApp + "-" + instType + "-" + str(x)
          if name not in instances.values():
              print "renaming -%s to %s" % (currentInstance, name)
              break

      for inst in currentInstance:
          inst.add_tag('Name', name)
          poutput = subprocess.check_output('hostname ' + name + '.cs.int', shell=True)
          sed_cmd = ("sed -i 's/HOSTNAME=.*/HOSTNAME={}.cs.int/' "
                    "/etc/sysconfig/network").format(name)
          poutput = subprocess.check_output(sed_cmd, shell=True)
          create_record('{}.cs.int'.format(name), "A", priv_ip, "Z1CTUH3DX45339", r53)
          create_record('{}.cs.int'.format(currentInstance[0]), "A", priv_ip, "Z1CTUH3DX45339", r53)
          create_record("{}.{}.30.172.in-addr.arpa.".format(priv_ip.split(".")[3], priv_ip.split(".")[2]),
            "PTR", '{}.cs.int'.format(name), "Z31KWMFMFZK6YQ", r53)
  - path: /usr/bin/allocate_eip.py
    content: |
      #!/usr/bin/python
      import requests
      import boto3
      import json
      
      instance_data = requests.get("http://169.254.169.254/latest/dynamic/instance-identity/document")
      response_json = instance_data.json()
      region = response_json.get('region')
      instance_id = response_json.get('instanceId')
      
      ec2 = boto3.client('ec2', region_name=region)

      try:
        allocate_eip = ec2.associate_address(AllocationId='eipalloc-0f7526dce6e0f1db8', InstanceId=instance_id)
      except:
        print("Associate IP failed")

      try:
        create_tag = ec2.create_tags(Resources=[instance_id], Tags=[{'Key':'ElasticIp', 'Value':'eipalloc-0f7526dce6e0f1db8'}])
      except:
        print("Create tag failed")

runcmd:
  - [ pip, install, boto3 ]
  - [ python, /usr/bin/rename_instance.py ]
  - [ sleep, 15 ]
  - [ python, /usr/bin/allocate_eip.py ]
  - [ service, sensu-client, stop ]
  - [ salt-call, saltutil.sync_all ]
  - [ salt-call, write_ec2tags.write_to_disk ]
  - [ salt-call, write_ec2tags.write_minion_id ]
  - [ salt-call, saltutil.revoke_auth ]
  - [ service, salt-minion, stop ]
  - [ rm, -rf, /etc/salt/pki/minion ]
  - [ rm, -rf, /opt/consul/data ]
  - [ rm, -rf, /var/lib/nomad/tmp/client ]
  - [ mv, /etc/salt/minion_id.tmp, /etc/salt/minion_id ]
  - [ cd, /tmp/tempcloudwatch ]
  - [ wget, "https://s3.amazonaws.com/amazoncloudwatch-agent/linux/amd64/latest/AmazonCloudWatchAgent.zip" ]
  - [ unzip, AmazonCloudWatchAgent.zip ]
  - [ sudo, ./install.sh ]
  - [ sudo, /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl, -a, fetch-config, -m, ec2, -c,"file:config.json", -s ]
  - [ service, salt-minion, start ]
  - [ sleep, 10 ]
  - [ salt-call, state.highstate ]