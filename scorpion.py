import sys
import exiftool
from time import sleep
#Aqui analizamos las imagenes para obtener los metadatos axif
#fuente: https://0x00sec.org/t/extracting-insights-from-data-how-to-build-a-metadata-scraper-for-digital-forensics-in-python/34436
def scorpio(file):
    print(file)
    with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(file)
        print(f"****************** METADATOS DEL ARCHIVO {file.upper()} ******************")
        for dict in metadata:
            for key, value in dict.items():
                print(f"{key:<45}:  {str(value)}")
            
    

if __name__=='__main__':
    for file in sys.argv[1:]:
        print(file)
        scorpio(file)