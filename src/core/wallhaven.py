import requests
from bs4 import BeautifulSoup 
from enum import Enum
import os

class Ratio(Enum):
    ALL = "all"
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"
    
    def __str__(self):
        return self.value
    
class ImageServer:
    """
    Equivalente de la clase ImageServer usada en el código B4A,
    que guarda la URL del preview y la imagen minimizada.
    """
    def __init__(self, preview_url, minimized_img):
        self.preview_url = preview_url
        self.minimized_img = minimized_img

class WallhavenScraper:
    """
    Adaptación de la clase en B4A a Python para extraer imágenes
    de Wallhaven usando requests y BeautifulSoup.
    """
    def __init__(self):
        self.home_url = "https://wallhaven.cc/"
        self.latest = self.home_url + "latest"
        self.hot = self.home_url + "hot"
        self.toplist = self.home_url + "toplist"
        self.random = self.home_url + "random"
        
        self.error_connection = False
        self.image_urls = []

    def open_image_view(self):
        """
        En B4A se llamaba StartActivity(Viewer). 
        En Python no hay equivalente directo para 'abrir actividad'.
        Puedes implementar lógica adicional si lo deseas.
        """
        print("open_image_view() llamado - sin implementación específica en Python.")

    def make_search(self, text, page=1, ratios=Ratio.ALL):
        """
        Traduce la lógica de MakeSearch() para generar la URL de búsqueda.
        """
        if text.startswith("id"):
            # Ejemplo: https://wallhaven.cc/search?q=id%3A175&sorting=random&ref=fp&page=1
            return f"{self.home_url}search?q={text}&sorting=random&ref=fp&page={page}&ratios={ratios}"
        elif text.startswith("tag"):
            # Ejemplo: https://wallhaven.cc/tag/96280&page=2
            tag_value = text.replace("tag:", "")
            return f"{self.home_url}tag/{tag_value}&page={page}&ratios={ratios}"
        else:
            # Ejemplo: https://wallhaven.cc/search?q=puppies&page=3 (reemplazando espacios por +)
            search_term = text.replace(" ", "+")
            return f"{self.home_url}search?q={search_term}&page={page}&ratios={ratios}"

    def make_page_url(self, base_url, page):
        """
        Traduce la lógica de MakePageUrl() para añadir ?page=N.
        """
        return f"{base_url}?page={page}"

    def get_image_4k(self, url):
        """
        Traduce la lógica de GetImage4K() usando requests + BeautifulSoup.
        - Conecta a la URL
        - Busca el elemento con id="wallpaper"
        - Obtiene el atributo src de la primera <img>
        """
        try:
            response = requests.get(url)
            response.raise_for_status()   
            soup = BeautifulSoup(response.text, 'html.parser')
             
            wallpaper_element = soup.find(id="wallpaper")
            if wallpaper_element: 
                return wallpaper_element["src"]
 
            return None
        except Exception as e:
            print("Ocurrió un error en get_image_4k:", e)
            return None

    def get_image_id(self, url):
        """
        Traduce la lógica de GetImageid() usando requests + BeautifulSoup.
        - Conecta a la id
        - Busca el elemento con id="wallpaper"
        - Obtiene el atributo src de la primera <img>
        """
        return os.path.splitext(os.path.basename(url))[0] 

    def get_images(self, url):
        """
        Traduce la lógica de GetImages() para:
        - Realizar la petición a la URL
        - Parsear y buscar cada <li> con <a class="preview"> e <img data-src="...">
        - Retornar la lista de ImageServer con preview_url y minimized_img
        """
        self.image_urls.clear()
        self.error_connection = False

        try: 
            response = requests.get(url)
            response.raise_for_status()
            html_main_source = response.text
 
            if not html_main_source.strip(): 
                self.error_connection = True
                return self.image_urls

            soup = BeautifulSoup(html_main_source, 'html.parser')
            li_elements = soup.find_all("li")

            for li in li_elements:
                try:
                    # Busca <a class="preview">
                    preview_link = li.find("a", class_="preview")
                    if preview_link:
                        # Busca <img> con data-src (la miniatura)
                        img_tag = li.find("img", attrs={"data-src": True})
                        if img_tag:
                            minimized_img = img_tag["data-src"]
                            preview_url = preview_link["href"]
                             
                            img_server = ImageServer(preview_url, minimized_img)
                            self.image_urls.append(img_server)
                except Exception as e:
                    print("Error procesando <li> individual:", e)

        except Exception as e:
            print("Error de conexión o parseo:", e)
            self.error_connection = True

        return self.image_urls
