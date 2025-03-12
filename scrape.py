import requests
from bs4 import BeautifulSoup
import mdutils

r = requests.get("https://pl.wikipedia.org/wiki/Korona_Europy")
r.text
soup = BeautifulSoup(r.text, "html.parser")
# f = open("down.html", 'w')
# print(soup.prettify())
# f.write(soup.prettify())
# f.close()

all_table_elements = soup.find_all("tr")

print(len(all_table_elements))
print(all_table_elements[20])

countries = []
for row in all_table_elements:
    countries.append(row.contents[3].find_all("a"))
countries2 = []
for row in countries:
    if len(row) > 0:
        countries2.append(row[0].string)
    else:
        countries2.append("None")
print(countries2)

mountains = ["None" for i in range(len(countries2))]
for i in range(len(all_table_elements)):
    mountains[i] = all_table_elements[i].contents[7]
mountains2 = ["None" for i in range(len(countries2))]
for i in range(len(all_table_elements)):
    if len(mountains[i].find_all("a")) != 0:
        mountains2[i] = mountains[i].find_all("a")[0].string
    else:
        mountains2[i] = mountains[i].string
    mountains2[i] = mountains2[i].replace("\n", "")
print(mountains2)


mntlist = mountains2[1:]
cntlist = countries2[1:]
sites = [0] * len(mntlist)
for i in range(len(mntlist)):
    sites[i] = mdutils.MdUtils(file_name="site" + str(i), title=mntlist[i])
    sites[i].create_md_file()


mdFile = mdutils.MdUtils(file_name="index.md", title="Lista Gor")

mdFile.new_header(level=1, title="Korona europy")
mdFile.new_header(level=2, title="Czyli najwyzsze szczyty 47 krajow europy")
table_content = []
for i in range(len(mntlist)):
    table_content.extend([i, cntlist[i], mdFile.new_inline_link(link = 'https://pancake5000.github.io/listagor/site' +str(i) + 'md', text = mntlist[i])])
print(table_content)
mdFile.new_table(
    columns=3, rows=len(table_content) // 3, text=table_content, text_align="center"
)
mdFile.create_md_file()
