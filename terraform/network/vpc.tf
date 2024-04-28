resource "aws_vpc" "myvpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "MyVPC"
  }
}

resource "aws_subnet" "PublicSubnet1" {
  vpc_id            = aws_vpc.myvpc.id
  availability_zone = "us-east-1a"
  cidr_block        = "10.0.1.0/24"

  tags = {
    Name = "PublicSubnet1"
  }
}

resource "aws_subnet" "PrivSubnet1" {
  vpc_id                  = aws_vpc.myvpc.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "PrivSubnet1"
  }
}

resource "aws_subnet" "PublicSubnet2" {
  vpc_id            = aws_vpc.myvpc.id
  availability_zone = "us-east-1b"
  cidr_block        = "10.0.3.0/24"

  tags = {
    Name = "PublicSubnet2"
  }
}

resource "aws_subnet" "PrivSubnet2" {
  vpc_id                  = aws_vpc.myvpc.id
  cidr_block              = "10.0.4.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "PrivSubnet2"
  }
}

resource "aws_internet_gateway" "myIgw" {
  vpc_id = aws_vpc.myvpc.id
}

resource "aws_route_table" "PublicRT" {
  vpc_id = aws_vpc.myvpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.myIgw.id
  }
}

resource "aws_route_table_association" "PublicRTAssociation1" {
  subnet_id      = aws_subnet.PublicSubnet1.id
  route_table_id = aws_route_table.PublicRT.id
}

resource "aws_route_table_association" "PublicRTAssociation2" {
  subnet_id      = aws_subnet.PublicSubnet2.id
  route_table_id = aws_route_table.PublicRT.id
}

resource "aws_eip" "lb" {
  vpc = true
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.lb.id
  subnet_id     = aws_subnet.PrivSubnet1.id

  tags = {
    Name = "gw NAT"
  }

  depends_on = [aws_internet_gateway.myIgw]
}