region = "us-east-1"

cluster_name = "mandalor-ecs-cluster"

service_name = "chip"

service_port = 8080

service_cpu = 256

service_memory = 512

service_launch_type = "EC2"

sservice_task_count = 3

ssm_vpc_id = "/mandalor-vpc/vpc/vpc_id"

ssm_listener = ""

ssm_private_subnet_1 = "/mandalor-vpc/vpc/subnet_private_1a"

ssm_private_subnet_2 = "/mandalor-vpc/vpc/subnet_private_1b"

ssm_private_subnet_3 = "/mandalor-vpc/vpc/subnet_private_1c"

service_hosts = [
  "chip.demo"
]

enviroment_variable = [
  {
    name  = "FOO"
    value = "BAR"
  },
  {
    name  = "PING"
    value = "PONG"
  },
]

capabilites = ["EC2"]

service_healthcheck = {
  health_threshold    = 3
  unhealthy_threshold = 10
  timeout             = 10
  interval            = 50
  matcher             = "200-399"
  path                = "/healthcheck"
  port                = 8080
}