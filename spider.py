from bs4 import BeautifulSoup
import requests
import os
import argparse
import pathlib
from urllib.parse import urlparse
from time import sleep

extensiones = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".docx", ".pdf"] #
attr_image_link = ["src", "srcset", "href", "style"]
tags_to_image = ["img", "image", "div"]
body_tags = ["a", "link"]
attr_body_tag = "href"
black_list_char = ["#"]

#url_root = https://www.42madrid.com

parser = argparse.ArgumentParser(description="Analizar la URL para obtener las imagenes")
parser.add_argument("URL", help="URL base para analizar")
parser.add_argument("-r", dest="recursiva", action="store_true", help="Descarga de forma recursiva las imagenes en la URL recibida.")
parser.add_argument("-l", dest="level", help="Indica el nivel de profundidad para la descarga recursiva.", type=int, default=5)
parser.add_argument("-p", dest="path", help="Indica el path donde se guardaran los archivos descargados", default="./data/")

params = parser.parse_args()

url_root = params.URL
recursividad = params.recursiva
level = params.level
if not recursividad: level = 0
path = params.path if params.path[-1] == '/' else params.path + '/'
url_parse = urlparse(url_root)
list_aux = []

def url_status_ok(url):
    try:
        return requests.get(url).status_code == 200
    except:
        return False

def create_list_of_string(string_of_urls, separator):
    return string_of_urls.split(separator)

def extract_images_links(image_tag):
    list_image_url = []
    list_url = []
    for attr in attr_image_link:
        if attr in image_tag.attrs.keys():
            list_image_url = create_list_of_string(image_tag[attr], " ")
        for url in list_image_url:
            list_url.append(url)
    return list_url


def create_image_name(url):
    split_url = url.split("/")
    return split_url[-1]

#Buscamos en la url las urls de las imagenes y las descargamos
def spider(url):
    if url_status_ok(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        folder_name = path

        #si no existe el directorio donde se almacenaran las imagenes, lo crea
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        
        #buscamos las etiquetas de la lista tags_to_image = ["img", "image"] utilizando soup.findAll
        for tag_image in tags_to_image:
            img = soup.findAll(tag_image)
            for image in img:
                list_images_urls =  extract_images_links(image)
                for image_url in list_images_urls:
                    #print(image_url)
                    image_url = urlparse(image_url)
                    image_name = create_image_name(image_url.path)
                    try:
                        response = requests.get(url_root + image_url.path) 
                        with open(f"{folder_name}{image_name}", "wb") as f:
                            f.write(response.content)
                    except:
                        continue

#------------- EXTRAER URLS DE UNA URL RAIZ ------------------------ www.42madrid.com
def extract_urls(url_root):
    if url_status_ok(url_root):
        lista_url = []
        response = requests.get(url_root)
        soup = BeautifulSoup(response.text, "html.parser")

        #buscamos las etiquetas de la lista body_tags = ["a", "link"] utilizando soup.findAll
        for url_tag in body_tags:
            for tag in soup.findAll(url_tag, href=True):
                str_attr_content = tag[attr_body_tag]
                if not any(char in str_attr_content for char in black_list_char):
                    if str_attr_content.startswith("/"):
                        str_attr_content = url_parse.scheme + "://" + url_parse.netloc + str_attr_content
                    if url_parse.netloc.rstrip("www.") in str_attr_content and str_attr_content not in list_aux:
                        #print(str_attr_content.rstrip("/"))
                        lista_url.append(str_attr_content.rstrip("/"))
                else:
                    continue 
        return lista_url
    else:
        return []


def search_url(url, lvl=0):
    global list_aux
    global num
    list_aux.append(url)
    if lvl < level:
        for u in extract_urls(url):
            if not u in list_aux:
                search_url(u, lvl + 1)        

def validate_url(url):
    url_parse = urlparse(url)
    if (url_parse.scheme and url_parse.netloc and url_status_ok(url)):
        return
    else:
        print(f"No se puede acceder a la URL: {url_root}. Contacte con el administrador del Servidor")
        exit()

#--------------------- MAIN -----------------------------
if __name__=="__main__":
    validate_url(url_root)
    print(f"Buscando y descargando imagenes del dominio {url_root}")
    if recursividad and level > 0:
        search_url(url_root)
        for url in list_aux:
            spider(url)
    elif level == 0:
        """ list_aux = extract_urls(url_root)
            for url in list_aux:
            print(url) """
        spider(url_root)
    print(f"La descarga se ha realizado correctamente.\nLas imagenes se encuentran en el PATH: {path}")


initial_count = 0
for folder in pathlib.Path(f"{path}").iterdir():
    if folder.is_file():
        initial_count += 1

print(initial_count)