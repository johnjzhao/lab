
resource "aws_glue_connection" "gov_solutions_commissions_glue_tdv_connection" {
  connection_properties = {
    JDBC_CONNECTION_URL = "jdbc:teradata://${var.gov_solutions_commissions_glue_config.host}/LOGMECH=LDAP"
    USERNAME            = "user"
    PASSWORD            = "password"
  }
  name            = "gov_solutions_commissions_glue_tdv_connection"
  connection_type = "JDBC"
  physical_connection_requirements {
    availability_zone      = "us-east-1b"
    security_group_id_list = [aws_security_group.gov_solutions_tdv_glue_sg.id]
    subnet_id              = data.aws_subnet.golden_vpc_subnets.id
  }
}