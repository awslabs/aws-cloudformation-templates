# CFNhelpernonAMZNAMIs
How can I install the CloudFormation helper scripts on non Amazon Linux AMIs? 


## Summary

How do I install the Cloudformation helper scripts in non Amazon Linux instances and how do I enable by default cfn-hup daemon in Systemd?
Main Text
Issue

I want to take advantage of the Cloudformation helper scripts in a non Amazon Linux instance.
Short Description

In order to use the Cloudformation helper scripts, you have to set the proper instructions to install them during the boot process as they are not included by default in non Amazon Linux AMIs.

For this you can use the easy_install command after installing both the Cloudformation bootstrap and python-setuptools packages.

## Resolution
Installing helper scripts through the Userdata property:
### Ubuntu 16.04 LTS
```
 "UserData" : { "Fn::Base64" : { "Fn::Join" : ["", [
             "#!/bin/bash -xe\n",
             "apt-get install -y python-setuptools\n",
             "mkdir -p /opt/aws/bin\n",
             "wget https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-latest.tar.gz\n",
             "easy_install --script-dir /opt/aws/bin aws-cfn-bootstrap-latest.tar.gz\n"
              ...
```
  
### RHEL 7
```
 "UserData": { "Fn::Base64" : { "Fn::Join" : ["", [
             "#!/bin/bash -xe\n",
             "apt-get update -y\n",
             "apt-get install -y python-setuptools\n",
             "mkdir -p /opt/aws/bin\n",
             "wget https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-latest.tar.gz\n",
             "easy_install --script-dir /opt/aws/bin aws-cfn-bootstrap-latest.tar.gz\n"
              ...
```

## Enabling cfn-hup in systemd.

Using the cfn-hup daemon allows you to make configuration updates on EC2 instances without needing to launch new ones.

It's a good practice to create a service in systemd for the cfn-hup daemon in order to start automatically at boot.

For systemd it must become a dependency of an existing boot target. You can use Multi-user.target which is similar to start on runlevel [2345] in upstart.


We set the instructions in the Metadata property files Key in order to create the cfn-hup configuration file, the cfn-hup hook, and the systemd file for cfn-hup /lib/systemd/systemcfn-hup.service.

We will use the commands key in order to enable the service in systemd and start it.
```
  "AWS::CloudFormation::Init" : {
          "configSets" : {
            "full_install" : [ "install_and_enable_cfn_hup" ]
          },
          "install_and_enable_cfn_hup" : {
            "files" : {
                        "/etc/cfn/cfn-hup.conf" : {
                          "content" : { "Fn::Join" : ["", [
                            "[main]\n",
                            "stack=", { "Ref" : "AWS::StackId" }, "\n",
                            "region=", { "Ref" : "AWS::Region" }, "\n"
                          ]]},
                          "mode"    : "000400",
                          "owner"   : "root",
                          "group"   : "root"
                        },
                        "/etc/cfn/hooks.d/cfn-auto-reloader.conf" : {
                          "content": { "Fn::Join" : ["", [
                            "[cfn-auto-reloader-hook]\n",
                            "triggers=post.update\n",
                            "path=Resources.EC2Instance.Metadata.AWS::CloudFormation::Init\n",
                            "action=/opt/aws/bin/cfn-init -v ",
                            "         --stack ", { "Ref" : "AWS::StackName" },
                            "         --resource EC2Instance ",
                            "         --configsets full_install ",
                            "         --region ", { "Ref" : "AWS::Region" }, "\n",
                            "runas=root\n"
                          ]]}
                        },
                       "/lib/systemd/system/cfn-hup.service": {
                            "content": { "Fn::Join" : ["", [
                            "[Unit]\n",
                            "Description=cfn-hup daemon\n\n",
                            "[Service]\n",
                            "Type=simple\n",
                            "ExecStart=/opt/aws/bin/cfn-hup\n", 
                            "Restart=always\n\n",
                            "[Install]\n",
                            "WantedBy=multi-user.target"]]}
                             }
                  },  
            "commands" : {
                  "01enable_cfn_hup" : {
                      "command" : "systemctl enable cfn-hup.service"
                  },
                  "02start_cfn_hup" : {
                      "command" : "systemctl start cfn-hup.service"
                  }
              }
           }
        }
```

You can verify after launching the stack that cfn-hup service has been started by executing systemctl status cfn-hup.

```
systemctl status cfn-hup
● cfn-hup.service - cfn-hup daemon
   Loaded: loaded (/usr/lib/systemd/system/cfn-hup.service; enabled; vendor preset: disabled)
   Active: active (running) since Wed 2016-10-12 08:10:26 EDT; 1min 11s ago
 Main PID: 4852 (cfn-hup)
   CGroup: /system.slice/cfn-hup.service
           └─4852 /usr/bin/python /opt/aws/bin/cfn-hup
Oct 12 08:10:26 ip-172-31-44-180.ec2.internal systemd[1]: Started cfn-hup daemon.
Oct 12 08:10:26 ip-172-31-44-180.ec2.internal systemd[1]: Starting cfn-hup daemon...
```
