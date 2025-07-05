variable "region" {
  default = "us-west-2"
}

variable "key_name" {
  description = "Name of the EC2 Key Pair"
}

variable "instance_type" {
  default = "t2.micro"
}
