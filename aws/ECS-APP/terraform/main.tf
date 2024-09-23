module "service" {
  source                      = "/home/thadeu/Documents/Projects/mandalor-containers-ecs-service-module"
  region                      = var.region
  cluster_name                = var.cluster_name
  service_name                = var.service_name
  service_port                = var.service_port
  servicec_cpu                = var.service_cpu
  servicec_memory             = var.service_memory
  service_listener            = data.aws_ssm_parameter.listener.value
  service_task_execution_role = aws_iam_role.main.arn
  service_healthcheck         = var.service_healthcheck
  service_launch_type         = var.service_launch_type
  service_task_count          = var.service_task_count
  service_hosts               = var.service_hosts

  enviroment_variables = var.enviroment_variables

  capabilites = var.capabilites

  vpc_id = data.aws_ssm_parameter.vpc.value
  private_subnets = [
    data.aws_ssm_parameter_subnet.private_subnets_1.value,
    data.aws_ssm_parameter_subnet.private_subnets_2.value,
    data.aws_ssm_parameter_subnet.private_subnets_3.value,
  ]

}