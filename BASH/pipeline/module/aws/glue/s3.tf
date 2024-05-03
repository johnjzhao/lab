#   This s3.tf file commented here for future use if needed 
#Creating S3 Bucket

resource "aws_s3_bucket" "gov-solutions-buckets" {
  acl    = "private"
  bucket = var.artifacts_bucket
  tags   = merge(var.cigna_common_tags, var.cigna_data_tags, var.required_tags)
  lifecycle {
    prevent_destroy = false
  }
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
  policy = <<EOF
 {
     "Id": "ArtifactsBucket",
     "Version": "2012-10-17",
     "Statement": [
         {
             "Sid": "AllowAccessWithSSLOnly",
             "Action": "s3:*",
             "Effect": "Deny",
             "Resource": [
                 "arn:aws:s3:::${var.artifacts_bucket}",
                 "arn:aws:s3:::${var.artifacts_bucket}/*"
             ],
             "Condition": {
                 "Bool": {
                      "aws:SecureTransport": "false"
                 }
             },
            "Principal": "*"
         }
     ]
 }
 EOF
}

resource "aws_s3_bucket_metric" "gov-solutions-buckets_metric" {
  bucket = var.artifacts_bucket
  name   = "GlueArtifactory"
}

resource "aws_s3_bucket" "evolve_to_commissions_bucket" {
  acl    = "private"
  bucket = var.vendor_bucket
  tags   = merge(var.cigna_common_tags, var.cigna_data_tags, var.required_tags)

  versioning {
    enabled = true
  }
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = aws_kms_key.secret_key.key_id
        sse_algorithm     = "aws:kms"
      }
      bucket_key_enabled = true
    }
  }
  policy = <<EOF
 {
     "Id": "VendorBucket",
     "Version": "2012-10-17",
     "Statement": [
         {
             "Sid": "AllowAccessWithSSLOnly",
             "Action": "s3:*",
             "Effect": "Deny",
             "Resource": [
                 "arn:aws:s3:::${var.vendor_bucket}",
                 "arn:aws:s3:::${var.vendor_bucket}/*"
             ],
             "Condition": {
                 "Bool": {
                      "aws:SecureTransport": "false"
                 }
             },
            "Principal": "*"
         },
         {
            "Sid": "AllowAccessToB2BRole",
            "Action": [
              "s3:List*",
              "s3:Get*"
            ],
            "Principal": {
              "AWS": "arn:aws:iam::${var.b2b_queue_aws_account}:role/B2BIONPREMCONNECTOR"
            },
            "Effect": "Allow",
            "Resource": [
                 "arn:aws:s3:::${var.vendor_bucket}",
                 "arn:aws:s3:::${var.vendor_bucket}/*"
            ]
         }
     ]
 }
 EOF
}

resource "aws_s3_bucket_object" "reports" {
  bucket       = var.vendor_bucket
  key          = "reports/"
  content_type = "application/x-directory"
}

# To be added back when b2b connection is setup for prod
#
# resource "aws_s3_bucket_notification" "s3_notification" {
#   bucket = aws_s3_bucket.evolve_to_commissions_bucket.id

#   queue {
#     queue_arn     = "arn:aws:sqs:us-east-1:${var.b2b_queue_aws_account}:mft-b2bi-s3event-work"
#     events        = ["s3:ObjectCreated:*"]
#     filter_prefix = "reports/"
#   }
# }

resource "aws_s3_bucket_metric" "evolve_to_commissions_bucket_metric" {
  bucket = var.vendor_bucket
  name   = "EntireBucket"
}