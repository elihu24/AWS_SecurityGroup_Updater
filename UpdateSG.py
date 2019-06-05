import boto3
import csv

#Variables to enter:
profile = "YOURAWSPROFILE" #default is created by default when you run aws configure from a terminal, allows for other than default
region = "YOURREGION"
security_group_id = "YOURSECURITYGROUP"
port_range_start = YOURSTARTPORT
port_range_end = YOURENDPORT
protocol = "YOURPRODOCOL"
csv_file = "YOURFILE.csv"

#Create lists
old_IP_list = []
new_IP_Master_List=[]

# Start a session, specifying profile credentials and region:
session = boto3.session.Session(profile_name=(profile),region_name=(region))
ec2 = session.resource('ec2')

#Produces a full description...https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#securitygroup
security_group = ec2.SecurityGroup(security_group_id)
boto_ec2 = boto3.client('ec2')

#Create master IP list from csv file = new_IP_Master_List:
with open(csv_file, 'r') as f:
  reader = csv.reader(f, delimiter=' ', quotechar='|')
  for row in reader:
      new_IP_Master_List.append(', '.join(row))

#Optional terminal output:
print("Master IP list: " + str(new_IP_Master_List))

#Create List of current IP rules = old_IP_list:
response = boto_ec2.describe_security_groups(GroupIds=[security_group_id])
for i in response['SecurityGroups']:
    for j in i['IpPermissions']:
               try:
                  for k in j['IpRanges']:
                      x = (k['CidrIp'])
                      old_IP_list.append(x[:-3])
               except Exception:
                  print ("No value for ports and ip ranges available for this security group")
                  continue

#Optional terminal output:
print("Current IP rules on AWS: " + str(old_IP_list))

#Compare both lists and remove only depricated IP rules only -- skip matches
for IP in old_IP_list: 
    #print("'" + str(IP) + "'")
    #print(old_IP_list)
    if IP in new_IP_Master_List: #in both - leave alone
        continue
    else:#act on IPs unique to old list (need to be revoked)
        security_group.revoke_ingress(
            DryRun=False,
            CidrIp=(IP + "/32"),
            IpProtocol=protocol,
            FromPort=port_range_start,
            ToPort=port_range_end
        )
        #Optional terminal output:
        print(str(IP) + " --removed from AWS")

#Compare both lists and add only new IP rules -- skip matches
for nIP in new_IP_Master_List:
    if nIP not in old_IP_list:
        cidr = (str(nIP) + "/32")
        security_group.authorize_ingress(
            DryRun=False,
            IpPermissions=[
                {
                    'FromPort': port_range_start,
                    'ToPort': port_range_end,
                    'IpProtocol': protocol,
                    'IpRanges': [
                        {
                            'CidrIp': cidr
                        },
                    ]
                }
            ]
        )
        #Optional terminal output:
        print(str(nIP) + " --added to AWS")
    else:
        #Optional terminal output:
        print(str(nIP) + " -- unchanged")
        continue
