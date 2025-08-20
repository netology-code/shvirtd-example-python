terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version = ">=1.5"
}

provider "yandex" {
  # token     = var.token
  cloud_id                 = "b1gk34aj8huam4c6qc65"
  folder_id                = "b1groq7lioh1rbih3b87"
  zone                     = "ru-central1-a"
  service_account_key_file = file("~/.authorized_key.json")
}
