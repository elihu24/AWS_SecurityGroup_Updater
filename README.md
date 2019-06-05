# AWS_SecurityGroup_Updater

Pass a masterlist of IPs to update the rules on a specific AWS SG; adds what doesn't exist, ignores what matches, and removes only what isn't on the master list

Script notes:
- Update the All caps parameters
- This script is designed to run on a security group that is hosting only one set of port ranges (i.e., every IP is allowed the same port/portrange) for an umbrella Security Group that would span multiple ec2 servers. (Think a masterlist of allowed SSH IPs for a fleet of servers.) Minor additional modification would need to be made to handle a Security Group with various kinds of ports/protocols allowed.


PERMISSIONS
Following AWS best practices, create a custom policy with the code below and attach this to the IAM user that will run the script:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "SGSpecific",
            "Effect": "Allow",
            "Action": [
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:RevokeSecurityGroupIngress",
                "ec2:RevokeSecurityGroupEgress"
            ],
            "Resource": "arn:aws:ec2:*:*:security-group/sg-0cbf3e235fdfcf762"
        },
        {
            "Sid": "DescribePermissions",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeSecurityGroups"
            ],
            "Resource": "*"
        }
    ]
}
