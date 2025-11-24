import requests
from PIL import Image
import io

dog_image_urls = [
    "https://images.dog.ceo/breeds/beagle/n02088364_11136.jpg",
    "https://images.dog.ceo/breeds/dalmatian/n02107166_10147.jpg",
    "https://images.dog.ceo/breeds/labrador/n02099712_5647.jpg",
    "https://images.dog.ceo/breeds/pug/n02110958_15553.jpg",
    "https://images.dog.ceo/breeds/shiba/shiba-13.jpg",
    "https://images.dog.ceo/breeds/husky/n02110185_1469.jpg",
    "https://images.dog.ceo/breeds/boxer/n02108089_1460.jpg",
    "https://images.dog.ceo/breeds/chihuahua/n02085620_3405.jpg",
    "https://images.dog.ceo/breeds/doberman/n02107166_6847.jpg",
    "https://images.dog.ceo/breeds/retriever-golden/n02099601_3002.jpg",
    "https://images.dog.ceo/breeds/germanshepherd/n02106662_3557.jpg",
    "https://images.dog.ceo/breeds/corgi-cardigan/n02113186_1016.jpg",
    "https://images.dog.ceo/breeds/bulldog-french/n02108915_10147.jpg",
    "https://images.dog.ceo/breeds/rottweiler/n02106550_10147.jpg",
    "https://images.dog.ceo/breeds/samoyed/n02111889_10147.jpg",
    "https://images.dog.ceo/breeds/pomeranian/n02112018_10147.jpg",
    "https://images.dog.ceo/breeds/malamute/n02110063_10147.jpg",
    "https://images.dog.ceo/breeds/dane-great/n02109047_10147.jpg",
    "https://images.dog.ceo/breeds/whippet/n02091134_10147.jpg",
    "https://images.dog.ceo/breeds/terrier-yorkshire/n02094433_10147.jpg"
]

bad = []
for url in dog_image_urls:
    r = requests.get(url)
    try:
        Image.open(io.BytesIO(r.content)).verify()
    except Exception:
        bad.append(url)

print("Bad images:", bad)
