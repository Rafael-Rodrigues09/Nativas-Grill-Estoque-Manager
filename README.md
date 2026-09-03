# - Sistema de Gestão de Estoque Perecíveis

## Links de Produção:
- Front-end (Interface): https://meat-estoque-manager-nativas.streamlit.app/
- Back-end (API Docs): https://nativas-grill-estoque-manager.onrender.com/docs

A interface do Streamlit implementa controle de visualização por perfil (RBAC). Para testar os diferentes fluxos na aplicação online, utilize as credenciais abaixo:

- Perfil Operador (Lançamentos rápidos de pesagem e reversão imediata): [INSIRA A USER_PASS DO .ENV]
- Perfil Administrador (Acesso ao histórico de auditoria, indicadores de reversão e relatórios): [INSIRA A ADMIN_PASS DO .ENV]

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
- Auditoria Imutável (Soft Rollback): A reversão de operações (/reverse) utiliza controle transacional LIFO sem deleção física no PostgreSQL. O registro original é mantido com a flag is_reversed = True, preservando 100% do histórico contábil para auditoria.
- Rotina EOD (End of Day): O sistema possui um gatilho de fechamento de turno que realiza o dump do banco, gera um arquivo de backup sanitizado em .pdf com timestamp e reseta a tabela para o turno seguinte.

## Como rodar localmente (Dev Environment)

O projeto utiliza o docker-compose para orquestração automática do banco de dados, API e Frontend em uma rede de contêineres isolada.

1. Clone este repositório:
- git clone https://github.com/Rafael-Rodrigues09/Meat-Estoque-Manager.git
- cd Meat-Estoque-Manager

2. Crie um arquivo .env na raiz do projeto contendo as seguintes variáveis:
- API_TOKEN=sua_senha_segura_da_api
- DATA_PASS=senha_do_banco_postgres
- DATA_URL=postgresql+psycopg2://postgres:${DATA_PASS}@db:5432/postgres
- USER_PASS=sua-senha-front-end
- ADMIN_PASS=sua-senha-historico
- API_URL=http://api:8000

3. Execute no terminal o Docker compose e suba a infraestrutura:
- docker compose up --build
