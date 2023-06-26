To access an EKS Cluster through kubectl assuming AWS Roles you must do the following:

1. Create the IAM Role that is going to be assumed by an aws user
   2. The role must have this trust entity policy. The ARN must be the ARN of the AWS User that will assume this role
       ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "Statement1",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": "arn:aws:iam::649165755582:user/cwoche-dev"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
       ```
   
2. Create the IAM Policy to attach to the IAM Role
    ```json
        {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowEKSAccess",
                "Effect": "Allow",
                "Action": [
                    "eks:AccessKubernetesApi",
                    "eks:Describe*",
                    "eks:List*"
                ],
                "Resource": "*"
            }
        ]
    }
   ```

3. Attach the policy to the Role

4. Create a new Policy that is going to be attached in the IAM User. Use the ARN of the role that you just created
    ```json
        {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowEKSRole",
                "Effect": "Allow",
                "Action": "sts:AssumeRole",
                "Resource": "arn:aws:iam::649165755582:role/EKSUserRole"
            }
        ]
    }
   ```
5. Attach the policy to the IAM User
6. The IAM User must have the permissions to use EKS. These are the permissions to use eksctl which covers the ones required to use EKS => https://eksctl.io/usage/minimum-iam-policies/
7. The role must be mapped to K8S through the iamIdentityMappings in the cluster.yaml