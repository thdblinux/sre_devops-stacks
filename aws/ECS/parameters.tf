resource "aws_ssm_parameter" "lb_arn" {
  name  = "/mandalor/ecs/lb/id"
  value = aws_lb.main.arn
  type  = "String"
}

resource "aws_ssm_parameter" "lb_listner" {
  name  = "/mandalor/ecs/lb/listner"
  value = aws_lb_listener.main.arn
  type  = "String"
}