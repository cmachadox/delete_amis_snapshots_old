import datetime
import boto3
import os

retention_days = os.environ['RETENTION_DAYS']
now = datetime.datetime.now() 
desired_retention = now - datetime.timedelta(days=int(retention_days))
ec2 = boto3.client('ec2') #ec2 manages AMIs and snapshots
account_id = os.environ['ACCOUNT_ID']

def deleteAMIs():
    amis_deleted = 0
    print("deleting AMIs")
    ami_list = ec2.describe_images(Owners=[str(account_id)],Filters=[{'Name':'image-type','Values':['machine']}])['Images']
    print("Ami availale in account - " + str(ami_list))
    for ami in ami_list:
        ami_creation_time = datetime.datetime.strptime(str(ami['CreationDate']),'%Y-%m-%dT%H:%M:%S.000Z')
        if desired_retention >= ami_creation_time:
            try:
                if "Tags" not in ami or "protegido" not in str(ami['Tags']):
                    ec2.deregister_image(ImageId=ami['ImageId'])
                    print("ami:",str(ami['ImageId']),str(ami['CreationDate']),"deleted")
                    amis_deleted += 1
                elif "protegido" in str(ami['Tags']):
                    print("protegido:", str(ami['ImageId']))
            except Exception as e:
                print("ERROR:",str(e))
    print(str(amis_deleted),"amis deletadas")

def deleteSnapshots():
    snapshots_deleted=0
    print("deleting snapshots")
    snapshots_list = ec2.describe_snapshots(OwnerIds=[str(account_id)])['Snapshots']
    print("Snapshots availale in account - " + str(snapshots_list))
    for snapshot in snapshots_list:
        snapshot_creation_time = datetime.datetime.strptime(str(snapshot['StartTime']),'%Y-%m-%d %H:%M:%S.%f+00:00')
        if desired_retention >= snapshot_creation_time:
            try:
                if "Tags" not in snapshot or "protegido" not in str(snapshot['Tags']) :
                    ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                    print("snapshot:",str(snapshot['SnapshotId']),str(snapshot['StartTime']),"deleted")
                    snapshots_deleted += 1
                elif "protegido" in str(snapshot['Tags']):
                    print("protegido:", str(snapshot['SnapshotId'])) 

            except Exception as e:
                print("ERROR:",str(e))
    print(str(snapshots_deleted),"snapshots deletados")

def handler(event, context):
    print("starting execution")
    #a deleção das AMIs precisa ocorrer antes. Você não consegue deletar um snapshot que tenha uma AMI o referenciando
    deleteAMIs()
    deleteSnapshots()
    return "AMIs and Snapshots deleted"
