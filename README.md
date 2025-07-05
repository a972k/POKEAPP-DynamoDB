# 🧬 Pokémon Drawer App – Cloud Edition

This project is a cloud-enabled Pokémon drawing game built in Python. It fetches Pokémon data from the [PokeAPI](https://pokeapi.co/) and stores it in **Amazon DynamoDB**. The app runs interactively on an **EC2 instance**, which can be deployed using either **Boto3** or **Terraform**.

---

## 🚀 Features

- 🎲 Draw random Pokémon from the PokeAPI
- 📥 Automatically store fetched data in DynamoDB
- 🔁 Avoid redundant API calls by reusing stored data
- ☁️ Launchable via:
  - Python + Boto3 (`fullappdeploy.py`)
  - Terraform (`terraform/` directory)
- 🔐 Secure with IAM roles for DynamoDB access
- 💬 Friendly command-line interaction

---

## 🧱 Technologies & AWS Services

| Technology      | Purpose                           |
|----------------|------------------------------------|
| Python          | Main application language          |
| Boto3           | AWS SDK for Python (used in app + EC2 provisioning) |
| PokeAPI         | External Pokémon data source       |
| DynamoDB        | NoSQL database to store Pokémon    |
| EC2             | Host and run the game              |
| IAM             | Secure EC2-to-DynamoDB access      |
| Terraform       | Infrastructure as Code (optional)  |

---

## 🧩 DynamoDB Schema

The app creates a table called `PokemonCollection` with the following attributes:

```json
{
  "name": "volbeat",
  "base_experience": 151,
  "abilities": ["illuminate", "swarm", "prankster"]
}
