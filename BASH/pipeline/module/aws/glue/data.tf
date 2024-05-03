
data "aws_vpc" "golden_vpc" {
  filter {
    name   = "tag:Name"
    values = ["gov-solutions-cigna-golden-vpc"]
  }
}

data "aws_subnet" "golden_vpc_subnets" {
  vpc_id = data.aws_vpc.golden_vpc.id

  filter {
    name   = "tag:Name"
    values = ["gov-solutions-cigna-golden-subnet-002"]
  }
}

data "aws_caller_identity" "current" {
}