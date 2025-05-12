# Tech Challenge 01

## Deploy

- O servidor está usando [Docker](https://www.docker.com/) para criar um container exclusivo para a aplicação
- [Documentação](/docker/README.md) da configuração usada para o Docker
- Para realizar um novo deploy, basta rodar a action [Docker Image CI](/.github/workflows/upload-docker-image.yml)
- A API atualizada estará disponível no subdomínio https://tc01.rteixeira.org/

## Segurança

- O acesso ao servidor está protegido por um proxy reverso usando [Zero Trust](https://www.cloudflare.com/pt-br/learning/security/glossary/what-is-zero-trust/) da [Cloudflare](https://www.cloudflare.com/pt-br/), impedindo que o IP do host seja identificado e também evitando ataques [DDoS](https://www.cloudflare.com/pt-br/ddos/)
