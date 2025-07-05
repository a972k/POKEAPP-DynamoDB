output "public_dns" {
  value = aws_instance.pokemon_game.public_dns
}

output "connect_command" {
  value = "ssh -i your-key.pem ec2-user@${aws_instance.pokemon_game.public_dns}"
}
