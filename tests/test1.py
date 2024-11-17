from src.wikipls import *

a = Article("Jamiroquai")
p = a.get_page(TEST_DATE)

print(f"{p.media}\n")
images = get_all_images(p.media, strict=False)
print(len(images))

with open("media_download_test.png", 'wb') as f:
    f.write(images[1])
