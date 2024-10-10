region = "us-east-1"

cluster_name = "mandalor-ecs-cluster"

service_name = "chip"

service_port = 8080

service_cpu = 256

service_memory = 512

service_launch_type = "EC2"

service_task_count = 3


ssm_vpc_id = "/mandalor-vpc/vpc/vpc_id"

ssm_listener = "/mandalor/ecs/lb/listener"

ssm_private_subnet_1 = "/mandalor-vpc/vpc/subnet_private_1a"

ssm_private_subnet_2 = "/mandalor-vpc/vpc/subnet_private_1b"

ssm_private_subnet_3 = "/mandalor-vpc/vpc/subnet_private_1c"

<<<<<<< Updated upstream:aws/ECS-APP/terraform/environment/dev/terraform.tfvars
ssm_alb             = "/mandalor/ecs/lb/id"
=======
ssm_alb = "mandalor/ecs/lb/id"
>>>>>>> Stashed changes:aws/ECS-APP/terraform/enviroment/dev/terraform.tfvars

service_hosts = [
  "chip.mandalor.demo"
]
environment_variables = [
  {
    Name  = "FOO",
    Value = "BAR"
  },
  {
    Name  = "PING",
    Value = "PONG"
  }
]

capabilities = ["EC2"]

service_healthcheck = {
  healthy_threshold   = 3
  unhealthy_threshold = 10
  path                = "/healthcheck"
  Port                = 8080
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
<<<<<<< Updated upstream:aws/ECS-APP/terraform/environment/dev/terraform.tfvars
scale_out_comparison_operator = "GreaterThanOrEqualToThreshold"
scale_out_statistic           = "Average"
=======
scale_out_comparison_operator = "GreaterThanOrEqualToThreshol"
scale_out_statistc            = "Average"
>>>>>>> Stashed changes:aws/ECS-APP/terraform/enviroment/dev/terraform.tfvars
scale_out_period              = 60
scale_out_evaluation_periods  = 2
scale_out_cooldown            = 60

<<<<<<< Updated upstream:aws/ECS-APP/terraform/environment/dev/terraform.tfvars
scale_in_cpu_threshold       = 30
scale_in_adjustment          = -1
scale_in_comparison_operator = "LessThanOrEqualToThreshold"
scale_in_statistic           = "Average"
scale_in_period              = 60
scale_in_evaluation_periods  = 2
scale_in_cooldown            = 60
=======
scale_in_cpu_threshold          = 30
scale_in_adjustment             = -1
scale_in_comparison_operator    = "LessThanOrEqualToThreshold"
scale_in_statistc               = "Average"
scale_in_period                 = 60
scale_in_cpu_evaluation_periods = 2
scale_in_cooldown               = 60
>>>>>>> Stashed changes:aws/ECS-APP/terraform/enviroment/dev/terraform.tfvars

scale_tracking_cpu      = 50
scale_tracking_requests = 30