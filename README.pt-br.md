<h1 align="center">Mlscraper - Um Web Scraper Construído em Python</h1>
<p align="center">
  <img src="scraper-logo.png" alt="ML-Scraper-logo" width="120px" height="120px"/>
  <br>
  <i>Este script é um exemplo de Web Scraper construído em
    <br>Python.</i>
  <br>
</p>




## Introdução


[![en](https://img.shields.io/badge/lang-en-red.svg?style=flat-square)](https://github.com/nothingnothings/mlscraper)
[![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg?style=flat-square)](https://github.com/nothingnothings/mlscraper/blob/master/README.pt-br.md)

Script construído em Python que extrai e armazena informações sobre os anúncios disponibilizados no site Mercado Livre em um banco de dados SQL containerizado. 

O Script utiliza scrapy para o scraping do site.

Para mais informações sobre sua utilização, leia as instruções abaixo.




## Tecnologias Utilizadas

- **Python**: A principal linguagem de programação utilizada.
- **Scrapy**: Biblioteca responsável pelo scraping
- **PyMySQL**: Biblioteca para conectar e interagir com bancos de dados MySQL.
- **MySQL**: Sistema de gerenciamento de banco de dados para armazenar dados de produtos.



## Instalação



1. Rode `git clone` para clonar o projeto dentro de seu repositório local Git



2. **Instale as Dependências**: Certifique-se de ter o Python instalado e execute:


```
pip install scrapy pymysql
```

3. O arquivo docker-compose.yml contém um banco de dados SQL pronto para uso. Para inicializá-lo, com o Docker instalado e em execução, digite os seguintes comandos:


```
cd docker
docker-compose up -d
```



## Uso


Para executar o scraper, execute os seguintes comandos:


```
cd mlscraper
scrapy crawl mlscraper -a s=<seu_termo_de_busca>
```


## Exemplo:

```
scrapy crawl mlscraper -a s=smartphone
```
