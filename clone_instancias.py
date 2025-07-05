import os
import time
import random
import requests
from github import Github

# CONFIGURAÇÕES GERAIS
GITHUB_TOKEN = "seu_github_token_aqui"  # Token de acesso ao GitHub
REPO_ORIGINAL = "seu_usuario/marcolacrueela"
QUANTIDADE_INSTANCIAS = 5
DELAY_ENTRE_CLONES = 60  # Segundos entre cada clone

def criar_fork(repo_name):
    g = Github(GITHUB_TOKEN)
    repo_original = g.get_repo(repo_name)
    fork = repo_original.create_fork()
    print(f"✅ Fork criado: {fork.html_url}")
    return fork.html_url

def iniciar_clone_no_railway(url_fork):
    railway_api_key = "sua_chave_de_api_do_railway_aqui"
    project_name = f"marcola_{random.randint(1000,9999)}"
    
    headers = {
        "Authorization": f"Bearer {railway_api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": project_name,
        "gitRepository": {
            "url": url_fork
        },
        "environmentVariables": [
            {"name": "TELEGRAM_TOKEN", "value": "7936846172:AAGkiPzf8XG5_TvRwZQJC3cVMudRd6UNMz0"}
        ]
    }

    response = requests.post(
        "https://api.railway.app/v1/projects ",
        headers=headers,
        json=payload
    )

    if response.status_code == 201:
        print(f"🚀 Projeto '{project_name}' iniciado no Railway.")
    else:
        print(f"❌ Erro ao criar projeto no Railway: {response.text}")

def main():
    for i in range(QUANTIDADE_INSTANCIAS):
        print(f"🔄 Criando clone #{i+1}...")
        url_fork = criar_fork(REPO_ORIGINAL)
        iniciar_clone_no_railway(url_fork)
        time.sleep(DELAY_ENTRE_CLONES)

if __name__ == "__main__":
    main()