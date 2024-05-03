# Boolean flag to create Transit Gateway attachment
tgw_attachment_enabled = true

#AWS CLI Profile to use for Terraform. SAML by default.
profile = "saml"

# Map of tags required for AWS resources. https://confluence.sys.cigna.com/display/CLOUD/Tags+for+all+AWS+Resources
cigna_common_tags = {
  SecurityReviewID = "RITM4181504"
  AppName          = "EDE-GOV-PRODUCER-COMMISSIONS"
  AssetName        = "gov-solutions-commissions"
  AssetOwner       = "EDEGOVARTETheSprintersTeam@Cigna.com"
  BackupOwner      = "john.zhao@evernorth.com"
  CiId             = "notAssigned"
  ServiceNowBA     = "BA17057"
  CostCenter       = "00790113"
  Purpose          = "Glue Infrastructure"
  Team             = "EDE GOV ART E The Sprinters Team"
  ServiceNowAS     = "AS040440"
  BusinessEntity   = "evernorth"
  LineOfBusiness   = "government"
}

cigna_data_tags = {
  DataSubjectArea        = "customer"
  ComplianceDataCategory = "pii:hipaa"
  DataClassification     = "internal"
}

required_tags = {
  AssetOwner       = "EDEGOVARTETheSprintersTeam@Cigna.com"
  CostCenter       = "00790113"
  SecurityReviewID = "RITM4181504"
  ServiceNowAS     = "AS040440"
  ServiceNowBA     = "BA17057"
}
