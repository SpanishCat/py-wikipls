from src.wikipls import *

a = Article("Pumped_Up_Kicks")
print(f"{a.details=}")
print(f"{a.id=}")
print(f"{a.name=}")
print(f"{a.key=}")
print(f"{a.content_model=}")
print(f"{a.license=}")
print(f"{a.latest=}")
print(f"{a.html_url=}")

p = a.get_page()

print(f"\n{p.name=}")
print(f"{p.name=}")
print(f"{p.date=}")
print(f"{p.lang=}")
print(f"{p.views=}")
print(f"{p.html[:20]=}")
print(f"{p.summary[:20]=}")
print(f"{p.media=}")
print(f"{p.as_pdf[:20]=}")
print(f"{p.data=}")

with open("test_pdf.pdf", 'wb') as f:
    f.write(p.as_pdf)
