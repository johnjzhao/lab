resource "aws_security_group" "gov_solutions_tdv_glue_sg" {
  name        = "gov-solutions-tdv-glue-${var.environment}-sg"
  description = "Security group for Glue connection"
  vpc_id      = data.aws_vpc.golden_vpc.id

  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    self      = "true"
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
    description = "Cigna Inbound"
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "ALL"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.cigna_common_tags, tomap({ "Name" = "gov-solutions-tdv-glue-${var.environment}-sg", "AssetName" = "GOV SOLUTIONS security group" }))
}