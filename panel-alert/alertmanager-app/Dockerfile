# Use a imagem do Ubuntu como base
FROM ubuntu:latest

# Atualize a lista de pacotes e instale o Python 3 e outras dependências
RUN apt-get update -y && \
  apt-get install -y python3-pip python3-dev default-libmysqlclient-dev && \
  apt-get clean

# Crie um diretório de trabalho para o projeto
WORKDIR /app

COPY . /app

# Instale as dependências do projeto
RUN pip3 install --upgrade pip && \
  pip3 install -r requirements.txt


# Defina o script entrypoint.sh como o entrypoint da imagem
ENTRYPOINT ["/bin/bash", "entrypoint.sh"]

# Expõe a porta do Flask
EXPOSE 5000
