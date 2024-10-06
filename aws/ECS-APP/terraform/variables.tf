variable "region" {
  type = string
}

variable "cluster_name" {
  type = string
}

variable "service_name" {
  type = string
}

variable "service_port" {
  type = number
}

variable "service_cpu" {
  type = number
}

variable "service_memory" {
  type = number
}

variable "service_healthcheck" {
  type = map(any) # Se você estiver passando um mapa para healthcheck
}

variable "service_launch_type" {
  type = string
}

variable "service_task_count" {
  type = number
}

variable "service_hosts" {
  type = list(string) # Se você estiver passando uma lista de strings
}

variable "ssm_vpc_id" {
  type = string
}

variable "ssm_listener" {
  type = string
}

variable "ssm_private_subnet_1" {
  type = string
}

variable "ssm_private_subnet_2" {
  type = string
}

variable "ssm_private_subnet_3" {
  type = string
}

variable "ssm_alb" {
  type        = string
  description = ""
}

variable "environment_variables" {
  type = list(map(string)) # Definindo como uma lista de mapas
}

variable "capabilities" {
  type = list(string) # Se você estiver passando uma lista de strings
}

variable "scale_type" {
  type = string
}

variable "task_minimum" {
  type = number
}

variable "task_maximum" {
  type = number
}

### Autoscaling de CPU

variable "scale_out_cpu_threshold" {}

variable "scale_out_adjustment" {}

variable "scale_out_comparison_operator" {}

variable "scale_out_statistic" {}

variable "scale_out_period" {}

variable "scale_out_evaluation_periods" {}

variable "scale_out_cooldown" {}

variable "scale_in_cpu_threshold" {}

variable "scale_in_adjustment" {}

variable "scale_in_comparison_operator" {}

variable "scale_in_statistic" {}

variable "scale_in_period" {}

variable "scale_in_evaluation_periods" {}

variable "scale_in_cooldown" {}


### Tracking CPU
variable "scale_tracking_cpu" {}


### Tracking Requests

variable "scale_tracking_requests" {}