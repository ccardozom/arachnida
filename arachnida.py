from spider import spider
from scorpio import scorpio

def main():
    url = f"https://www.42madrid.com/"
    folder = spider(url)
    scorpio(folder)

if __name__=="__main__":
    main()