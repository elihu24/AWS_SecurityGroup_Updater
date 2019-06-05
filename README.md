# AWS_SecurityGroup_Updater
Pass a masterlist of IPs to update the rules on a specific AWS SG; adds what doesn't exist, ignores what matches, and removes only what isn't on the master list

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
