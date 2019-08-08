# snappy-3000
This is a demo project to manage AWS instance snapshots using BOTO3 package

# Configuring
shotty uses configuration file created by AWS cli

`aws configure --profile shotty`

##Running

`pipenv run "python shotty/shotty.py" <command>
<subcommand> <--project=NAME>"`

*command* is instances, volumes, snapshots
*subcommand* is list, snapshot, start, stop
*project* is optional
