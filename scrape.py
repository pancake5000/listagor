import requests
from bs4 import BeautifulSoup
import mdutils
import mdutils
from duckduckgo_search import DDGS

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
heights = [0]*len(countries2)
for i in range(len(all_table_elements)):
    heights[i] = all_table_elements[i].contents[5].contents[0].string.replace("\n", "")
print(heights)
print(DDGS().images(keywords=mountains2[1], max_results=1))

mntlist = mountains2[1:]
cntlist = countries2[1:]
hgtlist = heights[1:]
sites = [0] * len(mntlist)
for i in range(len(mntlist)):
    sites[i] = mdutils.MdUtils(
        file_name="site" + str(i),
        title="---\ntitle: " + mntlist[i] + "\nlayout: default\npermalink: /site"+str(i)+".md/\n---\n" + mntlist[i],
    )
    # Perform DuckDuckGo image search
    if not (mntlist[i] == ""):
        if mntlist[i] == "bezimienny lub Iczka":
            results = DDGS().images(keywords="Iczka Kazachstan mountain", max_results=2)
        else:
            results = DDGS().images(keywords=mntlist[i] + ' ' + cntlist[i], max_results=2)
    image_urls = [result["image"] for result in results]

    # Add image URLs to the markdown file
    for url in image_urls:
        sites[i].new_paragraph(f"![{mntlist[i]}]({url})")
    f = open("site" + str(i) + ".md", "w")
    f.write(sites[i].get_md_text()[1:])
    # sites[i].create_md_file()


mdFile = mdutils.MdUtils(file_name="index.md",title ="---\ntitle: Korona Europy \nlayout: default\n---\n")
#mdFile.write("---\ntitle: Korona Europy \nlayout: default\n---")
#mdFile.new_header(level=1, title="Korona europy")
mdFile.new_header(level=1, title="Czyli najwyzsze szczyty 47 krajow europy")
table_content = ["", "Państwo","Wysokość w m n.p.m.", "Najwyższy Szczyt"]
for i in range(len(mntlist)):
    table_content.extend(
        [
            i+1,
            cntlist[i],
            hgtlist[i],
            mdFile.new_inline_link(
                link="https://pancake5000.github.io/listagor/site" + str(i) + ".md",
                text=mntlist[i],
            ),
        ]
    )
print(table_content)
mdFile.new_table(
    columns=4, rows=len(table_content) // 4, text=table_content, text_align="center"
)
f = open("index.md", "w")
f.write(mdFile.get_md_text()[1:])
#mdFile.create_md_file()
