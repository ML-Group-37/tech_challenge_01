## Build and upload image

- O workflow é responsável por gerar e subir a imagem mais recente do Docker no DockerHub
- É necessária a configuração no repositório do GitHub dos secrets `DOCKER_HUB_USERNAME` e `DOCKER_HUB_TOKEN` para realizar a autenticação no DockerHub
- É também necessária a configuração das variáveis `REGISTRY` e `IMAGE_NAME`, sendo a primeira do docker.io e a segunda para o nome da imagem
- Para rodar o workflow é necessário selecionar de qual branch será lido e em qual branch será executado
- 