provider "aws" {
  region = var.region
}

resource "aws_iam_role" "pokemon_role" {
  name = "pokemon_dynamo_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "attach_dynamodb_policy" {
  role       = aws_iam_role.pokemon_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_instance_profile" "pokemon_instance_profile" {
  name = "pokemon_instance_profile"
  role = aws_iam_role.pokemon_role.name
}

resource "aws_security_group" "pokemon_sg" {
  name        = "pokemon-sg"
  description = "Allow SSH"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "pokemon_game" {
  ami                    = "ami-04999cd8f2624f834"  # Amazon Linux 2 in us-west-2
  instance_type          = var.instance_type
  key_name               = var.key_name
  security_groups        = [aws_security_group.pokemon_sg.name]
  iam_instance_profile   = aws_iam_instance_profile.pokemon_instance_profile.name
  user_data              = file("user_data.sh")

  tags = {
    Name = "PokemonGameInstance"
  }
}
