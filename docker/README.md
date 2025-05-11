## Dockerfile

- Estamos utilizando a imagem base the python python:3.9-slim
- Adicionamos as bibliotecas necessárias no arquivo [requirements.txt](../tech_challenge/requirements.txt)
- Na construção do container utilizamos co comando `pip install` para instalar as dependências listadas no arquivo
- O serviço é exposto por padrão na porta **8000**

## Docker compose

- Está buscando no DockerHub a imagem mais recente do repositório [rtexa/ml-group-37-tech-challenge-01](https://hub.docker.com/r/rtexa/ml-group-37-tech-challenge-01)
- Altera a porta do host de **8000** para **9123**
- Roda também em paralelo o serviço [Watchtower](https://github.com/containrrr/watchtower), responsável por verificar se há uma nova imagem do nosso serviço disponível, automaticamente reiniciando e atualizando o container
- 