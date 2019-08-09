import boto3
import click

session = boto3.Session(profile_name = 'shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []
    if project:
        filters = [{'Name':'tag:proj', 'Values':[project]}]
        instances = ec2.instances.filter(Filters = filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def cli():
    """Commands for Command line interface"""

@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

@snapshots.command('list')

@click.option('--project', default=None,
    help="Only snapshots for project (tag proj:<name>)")
def snapshots_call(project):
    "List EC2 instances' volumes' snapshots"
    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(', '.join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime('%c')
                )))

    return


@cli.group('volumes')
def volumes():
    """Commands for volumes"""

@volumes.command('list')

@click.option('--project', default=None,
    help="Only volumes for project (tag proj:<name>)")
def volumes_call(project):
    "List EC2 instances' volumes"
    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            tags = { t['Key']: t['Value'] for t in i.tags or [] }
            print(', '.join((
                v.id,
                i.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
                )))

    return

@cli.group('instances')
def instances():
    """Commands for instances"""

@instances.command('snapshot', help="create snapshots for all volumes")

@click.option('--project', default=None,
    help="Only instances for project (tag proj:<name>)")
def create_snapshots(project):
    "create snapshot for all EC2 instances"
    instances = filter_instances(project)
    for i in instances:
        print("Stopping inst # {}....".format(i.id))
        i.stop()
        i.wait_until_stopped()

        for v in i.volumes.all():
            print("Creating snapshots for in volumes {}".format(v.id))
            v.create_snapshot(Description="Created by my program to create CLI")

        print("Starting inst {}".format(i.id))

        i.start()
        i.wait_until_running()

    print("Job done!!")

    return


@instances.command('list')

@click.option('--project', default=None,
    help="Only instances for project (tag proj:<name>)")
def list_call(project):
    "List EC2 instances"
    instances = filter_instances(project)
    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('proj', '<no project>')
            )))

    return


@instances.command('stop')

@click.option('--project', default=None,
    help="Only instances for project (tag proj:<name>)")
def stop_call(project):
    "stop EC2 instances"
    instances = filter_instances(project)

    for i in instances:
        print("stopping {}".format(i.id))
        i.stop()

    return


@instances.command('start')

@click.option('--project', default=None,
    help="Only instances for project (tag proj:<name>)")
def start_call(project):
    "start EC2 instances"
    instances = filter_instances(project)

    for i in instances:
        print("starting {}".format(i.id))
        i.start()

    return

if __name__ == '__main__':
    cli()
