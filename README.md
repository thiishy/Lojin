# 🛒 Lojin - API demo de pipeline CI/CD completo

<div align="center">

   ![Python](https://img.shields.io/badge/Python-ED8B00?logo=python&logoColor=white)
   ![FastAPI](https://img.shields.io/badge/FastAPI-009485?logo=fastapi&logoColor=white)
   ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white)
   ![Docker](https://img.shields.io/badge/Docker-257bd6?logo=docker&logoColor=white)
   ![GitHub Actions](https://img.shields.io/badge/GitHub-000000?logo=github&logoColor=white)

   ![Imagem demonstrando a documentação da API no Swagger](https://i.imgur.com/xdGfkEs.png)

O Lojin é uma API demo desenvolvida em Python com FastAPI para a aula de Integração e Entrega Contínua na Fatec Praia Grande. O objetivo do projeto é demonstrar um pipeline CI/CD completo funcionando dos testes até o deploy para a nuvem utilizando Docker e GitHub Actions.

</div>

## 📦 Pré-requisitos

#### Manual (sem Docker/Podman)
- 🌿 **Git** *(opcional)* [(Download)](https://git-scm.com/install/)
- 🐍 **Python 3.14+** e **pip** [(Download)](https://www.python.org/downloads/)
- 🐘 **PostgreSQL 17+** [(Download)](https://www.postgresql.org/download/)

#### O caminho fácil (com Docker/Podman) *(recomendado)*
- 🌿 **Git** *(opcional)* [(Download)](https://git-scm.com/install/)
- 🐋🦭 **Docker/Docker Compose** *ou* **Podman/Podman Compose** [(Download do Docker)](https://www.docker.com/get-started/) **|** [(Download do Podman)](https://podman.io/)

## ⚙️ Configuração
### Manual (sem Docker/Podman)
1. Instale o Python 3.14+ e o PostgreSQL 17+
2. Configure o banco de dados
3. Clone o repositório (pelo website ou com o comando `git clone https://github.com/thiishy/Lojin.git` caso tenha instalado o Git)
4. Na pasta `src/`, crie um arquivo **.env** seguindo o template que está no arquivo **.env.example**:
   - **DB_NAME**: Nome do banco de dados
   - **DB_USERNAME**: Nome do seu usuário no banco de dados
   - **DB_PASSWORD**: Senha do seu usuário no banco de dados
   - **DATABASE_URL**: URL da conexão com o banco de dados *(ex: postgresql://nome:senha@host/banco)*

   Após isso, rode o comando `pip install -r requirements.txt` para instalar os pacotes Python necessários
5. Para inicializar a aplicação, rode `uvicorn main:app`. Use o parâmetro `--reload` para habilitar o recarregamento automático caso haja mudanças no código

### O caminho fácil (com Docker/Podman)
1. Instale o Docker/Docker Compose *ou* Podman/Podman Compose
2. Clone o repositório (pelo website ou com o comando `git clone https://github.com/thiishy/Lojin.git` caso tenha instalado o Git)
3. Na pasta `src/`, crie um arquivo **.env** seguindo o template que está no arquivo **.env.example**. Note que o banco de dados será **configurado automaticamente** pelo Docker/Podman Compose com os dados que você escolher aqui:
   - **DB_NAME**: Nome do banco de dados
   - **DB_USERNAME**: Nome do seu usuário no banco de dados
   - **DB_PASSWORD**: Senha do seu usuário no banco de dados
   - **DATABASE_URL**: URL da conexão com o banco de dados. Não use `localhost`, use `db` para referenciar o host do banco de dados. *(ex: postgresql://nome:senha@db/banco)*

   Após isso, rode o comando `docker-compose up --build`**/**`podman-compose up --build` e aguarde

4. A aplicação irá iniciar automaticamente. Você pode parar os serviços com `docker-compose stop`**/**`podman-compose down` ou apagar os containers com `docker-compose down`**/**`podman-compose down` (**não apaga** os volumes) ou `docker-compose down -v`**/**`podman-compose down -v` (**apaga** os volumes)

## 🔗 Como acessar

Após a configuração, você pode acessar a documentação da API e testar em:
- **http://localhost:8000/docs** **(Swagger UI - ilustrada acima)**
- **http://localhost:8000/redoc** **(ReDoc)**

## 🛠️ Funcionalidades
- Listar, criar, buscar, atualizar e apagar produtos
- Aplicar descontos fixos (R$) e em porcentagem

## 🏗️ Pipeline

Explicação do pipeline CI/CD localizado em `.github/workflows/pipeline.yml`. Os três jobs rodam em um container com a última versão do Ubuntu, e o pipeline só é executado em caso de **push** na branch `main` E na pasta `src/`.

### 🗄️ Especificações do VPS utilizado

Droplet do DigitalOcean rodando Ubuntu 24.04 LTS x64, 4 Intel vCPU, 8 GB RAM, 240 GB NVMe SSD.

Docker rodando sem root (usuário no grupo `docker`) e PostgreSQL 17 hospedado manualmente (Docker Compose/Podman Compose não foi utilizado).

Não foi testado com Podman, mas deve funcionar também.

### 1️⃣ Job de testes (test)
1. Faz o checkout do repositório;
2. Configura o **Python** na versão **3.14**;
3. Atualiza o **pip** e instala todos os requisitos da aplicação a partir do arquivo **requirements.txt**;
4. Executa os testes unitários (aplicação de descontos) e testes de integração (respostas esperadas da API) utilizando o **pytest** junto a um banco SQLite na memória;
5. Verifica se os pacotes contém alguma vulnerabilidade com o **pip-audit**;
6. Executa a ferramenta de lint **black**, checando se o código está nos padrões da [PEP 8](https://peps.python.org/pep-0008/).

### 2️⃣ Job de build e push da imagem Docker (build-and-push)

Precisa do **sucesso** do job de testes (test) para executar.

1. Faz o checkout do repositório;
2. Realiza o login no **Docker Hub**, pegando o usuário e token dos secrets do GitHub;
3. Builda a imagem e a envia para o Docker Hub *(ex: usuario/lojin:latest)*.

### 3️⃣ Job de deploy para a nuvem (deploy)

Precisa do **sucesso** do job de build e push da imagem Docker (build-and-push) para executar.

1. Estabelece uma **conexão SSH** com o VPS fornecendo o host, usuário e senha (embora o ideal seja usar uma chave SSH);
2. Puxa a imagem mais recente do **Docker Hub**;
3. Para e apaga o container antigo;
4. Executa o container novo, passando como variável de ambiente a URL de conexão do banco de dados, guardada em um secret do GitHub.

---

Feito com ♥ por [thiishy](https://github.com/thiishy)