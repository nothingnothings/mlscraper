<h1 align="center">Mlscraper - A Web Scraper Built with Python</h1>
<p align="center">
  <img src="scraper-logo.png" alt="ML-Scraper-logo" width="120px" height="120px"/>
  <br>
  <i>This script is an example of a Web Scraper Built with
    <br>Python.</i>
  <br>
</p>


## Introduction

[![en](https://img.shields.io/badge/lang-en-red.svg?style=flat-square)](https://github.com/nothingnothings/mlscraper)
[![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg?style=flat-square)](https://github.com/nothingnothings/mlscraper/blob/master/README.pt-br.md)

Script built with Python that extracts and stores data about the Mercado Livre website's data in a containerized SQL database.

The script uses scrapy for the website's scraping.

For more information about its usage, read the instructions below.


## Technologies Used


- **Python**: The primary programming language used.
- **Scrapy**: Library responsible for the scraping
- **PyMySQL**: Library for connecting to and interacting with MySQL databases.
- **MySQL**: Database management system for storing product data.



## Installation

1. Run `git clone` to clone the project into your local Git repository.


2. **Install Requirements**: Make sure you have Python installed and run:


```bash 
pip install scrapy pymysql
```

3. The docker-compose.yml file contains a ready-to-use SQL database. To initialize it, with Docker installed and running, type the following commands:


```
cd docker
docker-compose up -d
```


## Usage

To run the scraper, execute the following commands:

```
cd mlscraper
scrapy crawl mlscraper -a s=<your_search_term>
```


## Example:

```
scrapy crawl mlscraper -a s=smartphone
```
