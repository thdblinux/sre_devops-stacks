output "load_balancer_dns" {
  value = aws_lb.main.dns_name
}

output "lb_ssm_arn" {
  value = aws_ssm_parameter.lb_arn.id
}


output "lb_ssm_listner" {
  value = aws_ssm_parameter.lb_listner.id
}