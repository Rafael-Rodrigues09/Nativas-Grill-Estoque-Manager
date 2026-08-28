# - Sistema de Gestão de Estoque Perecíveis

## Links de Produção:
- Front-end (Interface): https://nativas-grill-estoque-manager-2ll7.onrender.com
- Back-end (API Docs): https://nativas-grill-estoque-manager.onrender.com

⚠️ **Aviso** (Cold Start): Este projeto está hospedado no plano gratuito do Render. Por padrão, os contêineres entram em hibernação após 15 minutos de inatividade. O primeiro acesso pode levar cerca de **50 segundos** para acordar a API e o Banco de Dados. Abrir o link da API primeiro, aguardar o carregamento e, em seguida, acessar o Front-end para evitar erros.

## Contexto Operacional (O Problema)
O controle de estoque no setor de perecíveis (carnes) em ambientes de alta demanda (churrascarias) é tradicionalmente feito de forma manual em papel. Esse método gera perda de histórico, inconsistência de dados e falhas de auditoria. 

Este projeto foi desenvolvido para substituir a prancheta física por um sistema digital, persistente, conteinerizado e de alta disponibilidade.

## Arquitetura do Sistema
A aplicação foi arquitetada sob o modelo de Microserviços Desacoplados, separando totalmente as responsabilidades de interface, regras de negócio e persistência de dados. O projeto está estruturado em um formato de Monorepo.

## Stack Tecnológica:
- Back-end (API): Python, FastAPI (Arquitetura assíncrona, injeção de dependência e validação estrita com Pydantic).
- Banco de Dados: PostgreSQL isolado com persistência de volumes.
- ORM: SQLAlchemy 2.0 para mapeamento objeto-relacional seguro contra SQL Injection.
- Front-end: Streamlit (Dumb Client consumindo a API RESTful via requests HTTP).
- Infraestrutura / DevOps: Docker, Docker Compose e Deploy na nuvem (Render) com Zero Downtime.

## Regras de Negócio e Segurança
- Isolamento de Estado: O front-end não possui conexão com o banco de dados. Toda requisição passa obrigatoriamente pela API.
- Segurança de Rotas: As rotas de mutação (POST/UPDATE) são protegidas por autenticação via Headers (x-token), validados através de variáveis de ambiente (.env).
- Rotina EOD (End of Day): O sistema possui um gatilho de fechamento de turno que realiza o dump do banco, gera um arquivo de backup sanitizado em .txt com timestamp e reseta a tabela para o turno seguinte.

## Como rodar localmente (Dev Environment)

O projeto utiliza o docker-compose para orquestração automática do banco de dados, API e Frontend em uma rede de contêineres isolada.

1. Clone este repositório:
- git clone https://github.com/Rafael-Rodrigues09/Meat-Estoque-Manager.git
- cd Meat-Estoque-Manager

2. Crie um arquivo .env na raiz do projeto contendo as seguintes variáveis:
- API_TOKEN=sua_senha_segura_da_api
- DATA_PASS=senha_do_banco_postgres
- DATA_URL=postgresql+psycopg2://postgres:${senha_do_banco_postgres}@db:5432/postgres
- USER_PASS=sua-senha-front-end
- ADMIN_PASS=sua-senha-historico
- API_URL=http://api:8000

3. Execute no terminal o Docker compose e suba a infraestrutura:
- docker compose up --build
