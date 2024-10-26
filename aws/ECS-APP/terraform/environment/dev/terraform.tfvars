region = "us-east-1"

cluster_name = "mandalor-ecs-cluster"

service_name = "chip"

service_port = 8080

service_cpu    = 256
service_memory = 512

# Ajuste o tipo de lançamento para uma string, como "FARGATE" ou "FARGATE_SPOT"
service_launch_type = [
  {
    capacity_provider = "FARGATE"
    weight            = 50
  },
  {
    capacity_provider = "FARGATE_SPOT"
    weight            = 50
  }

]

service_task_count = 3

ssm_vpc_id = "/mandalor-vpc/vpc/vpc_id"

ssm_listener = "/mandalor/ecs/lb/listener"

ssm_private_subnet_1 = "/mandalor-vpc/vpc/subnet_private_1a"

ssm_private_subnet_2 = "/mandalor-vpc/vpc/subnet_private_1b"

ssm_private_subnet_3 = "/mandalor-vpc/vpc/subnet_private_1c"

ssm_alb = "/mandalor/ecs/lb/id"

service_hosts = [
  "chip.mandalor.demo"
]

environment_variables = [
]

# As capacidades devem ser compatíveis com o tipo de lançamento Fargate
capabilities = ["EC2"] # Altere para "FARGATE" se estiver usando Fargate

service_healthcheck = {
  healthy_threshold   = 3
  unhealthy_threshold = 10
  path                = "/healthcheck"
  port                = 8080
  timeout             = 10
  interval            = 60
  matcher             = "200-399"
}

scale_type   = "requests_tracking"
task_minimum = 3
task_maximum = 12

### Autoscaling de CPU

scale_out_cpu_threshold       = 50
scale_out_adjustment          = 2
scale_out_comparison_operator = "GreaterThanOrEqualToThreshold"
scale_out_statistic           = "Average"
scale_out_period              = 60
scale_out_evaluation_periods  = 2
scale_out_cooldown            = 60

scale_in_cpu_threshold       = 30
scale_in_adjustment          = -1
scale_in_comparison_operator = "LessThanOrEqualToThreshold"
scale_in_statistic           = "Average"
scale_in_period              = 60
scale_in_evaluation_periods  = 2
scale_in_cooldown            = 60

scale_tracking_cpu      = 50
scale_tracking_requests = 30

ssm_service_discovery_namespace = "/mandalor/ecs/cloudmap/namespace"