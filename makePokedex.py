#! /usr/bin/python3
print("Content-Type: text/html\n\n")

# this tells Python to treat the file as UTF-8 encoded which supports all special characters.

import cgitb # import to catch HTTP errors (when running on the web)
cgitb.enable() # enable your error output for HTTP
path="/home/students/odd/2027/azeleniy70/public_html/pokemon"
indent = '  '
page = '''
<!DOCTYPE html>
<html>
  <head>
    _STYLE_ 
    <title>_TITLE_</title> 
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
  </head>
  <body>
    _NAVBAR_
    _BODY_
  </body>
</html>'''

nav_items = [
    ["Home", "makePokedex.py"],
    ["Top 10", "HTML/top10.html"],
    ["All Pokemon", "HTML/allpokemon.html"],
    ["Types", "submenu"]
]

pages_to_make = ["Top 10", "All Pokemon"]

# try change makeNavbar to using multiline

def makeNavbar(nav_items, depth):
    prefix = "../" * depth  # calculate how deep the current page is relative to makePokedex.py
    nav_template = '''<nav>
        <ol>
            _NAV_ITEMS_
        </ol>
    </nav>'''
    nav_items_str = ""

    for item in nav_items:
        label = item[0] # name goes first slot
        target = item[1] # 2nd slot is basically either gonna be a link or gonna be submenu
                         # if it's submenu, we have our submenu as a list of lists in third slot
        if target == "submenu":
            submenu = item[2]
            nav_items_str += f"{indent*3}<li>{label}\n"
            nav_items_str += f"{indent*4}<ul>\n"
            for sub in submenu:
                sub_label = sub[0]
                sub_link = prefix + sub[1] # apply prefix
                nav_items_str += f'{indent*5}<li><a href="{sub_link}">{sub_label}</a></li>\n'
            nav_items_str += f"{indent*4}</ul>\n"
            nav_items_str += f"{indent*3}</li>\n"
        else:
            link = prefix + target # apply prefix to top level link
            nav_items_str += f'{indent*4}<li><a href="{link}">{label}</a></li>\n'
    
    final_nav = nav_template.replace("_NAV_ITEMS_", nav_items_str.strip())

    return final_nav


def makeTable(caption_text, headers, data):
    # Define the table template
    Htable = '''<table border=1>
      <caption>_TCAPTION_</caption>
      <thead>
        <tr>
          _THEADERS_
        </tr>
      </thead>
      <tbody>
        _TITEMS_
      </tbody>
    </table>'''

    # Generate headers
    headers_str = ""
    for header in headers:
        headers_str += indent * 5 + "<th>" + header + "</th>\n"

    # Generate table rows
    items_str = ""
    for row in data:
        td_row = ""
        for cell in row:
            td_row += indent * 5 + "<td>" + str(cell) + "</td>\n"
        
        # Remove last newline to avoid extra spacing
        td_row = td_row[:-1]
        items_str += indent * 4 + "<tr>\n" + td_row + "\n" + indent * 4 + "</tr>\n"

    # Replace placeholders
    Htable = Htable.replace("_TCAPTION_", caption_text)
    Htable = Htable.replace("_THEADERS_", headers_str.strip())
    Htable = Htable.replace("_TITEMS_", items_str.strip())

    return Htable

def makeHeader(h,num):
    return "<h"+str(num)+">"+str(h)+"</h"+str(num)+">\n"

def makeParagraph(p):
    global indent
    return indent * 2 + "<p>"+str(p)+"</p>"


# this function reads entire file and adds images and returns a list of lists where each sublist is a row
def readWholeFile():  # i made it seperate since it's used when making each page so more useful as it's own function
    file = open(f"{path}/pokemon.csv")
    wholeFileList = []
    for line in file:
        row = (line.strip()).split(',')
        wholeFileList.append(row)
    wholeFileList[0].insert(1, "front")   # also does the imaging
    wholeFileList[0].insert(2, "back")
    for pokemon in wholeFileList[1:]:
        pokemon.insert(1, f"<img src='../img/front/{pokemon[0]}.png'/>")
        pokemon.insert(2, f"<img src='../img/back/{pokemon[0]}.png'/>")
    return wholeFileList

myFileList = readWholeFile()

def makeHomeBody(): # function makes homepage
    for row in myFileList:
        if row[3] == "Chansey":   # search for Chansey number
            favPokerow = int(row[0])

    favPokemon = myFileList[favPokerow]  
    favPokemon[1] = f"<img src= 'img/front/{favPokerow}.png'/>"   
    favPokemon[2] = f"<img src= 'img/back/{favPokerow}.png'/>"   # need to do this to locate updated path for img since not going from inside HTML


    homepg = makeHeader("Pokedex Homepage",1)
    homepg += makeParagraph("""My favorite pokemon is Chansey because he is the highest ranking pokemon from my formula, of multiplying total stats by health. 
    Chansey is a super rare and gentle Pokemon from Generation 1. She’s known for her massive HP and healing abilities.
    She carries a special egg in her pouch, which is said to bring happiness to anyone who eats it.""")
    homepg += makeTable("", myFileList[0], [favPokemon])  # put a list around favpokemon cuz my makeTable takes list of lists for content
    homepg += "<img class = 'gif' src=wchansey.gif>"

    return  homepg 

def allpokemonBody():  # this function makes the body for all pokemon page
    allpg = makeHeader("All Pokemon",1)
    allpg += makeParagraph("""Personally, I’ve always liked Pokemon. 
    The idea of making your own team of creatures and battling friends is just so fun. 
    I especially love the original version because the designs were simpler and the nostalgia is unbeatable.
    """)
    allpg += makeTable("", myFileList[0], myFileList[1:])
    return allpg


def totalTimesHP(row): # calculate the total * hp for a single row and return the result, used to rank top 10
    total = int(row[6])
    hp = int(row[7])
    return total * hp  

def top10Body():  # makes the top 10 body page

    # Sort the rows based on total * hp using the totalTimesHP function
    sorted_rows = sorted(myFileList[1:], key=totalTimesHP, reverse=True)

    # Get the top 10 Pokémon (by highest total * hp)
    top10list = sorted_rows[:10]
    top10pg = makeHeader("Top 10 Pokemon",1)
    top10pg += makeParagraph("""Here’s a list of the top 10 Pokemon, sorted by their total stat value multiplied by their HP. 
    I picked these because this method combines both total stats and health, (with a slight emphasis on health) giving us a better idea of which Pokémon are the toughest overall.
    It’s cool because it doesn’t just look at one stat; it considers all of them. 
    These 10 Pokemon stand out as the strongest when you factor in both their power and endurance!""")
    top10pg += makeTable("", myFileList[0], top10list)
    return top10pg

def makeTop10andAllPages():
    for item in nav_items:
        if item[0] in pages_to_make:
            label = item[0]
            filename = item[1]
            function_name = label.replace(" ", "").lower() + "Body"  # allPokemonBody, top10Body
            try:
                body_func = globals()[function_name]
                body_html = body_func()
                with open(filename, "w") as f:
                    page_html = page.replace("_STYLE_", '<link href="../CSS/PokeStyle.css" rel="stylesheet" type="text/css">')
                    #
                    page_html = page_html.replace("_NAVBAR_", makeNavbar(nav_items, 1))
                    page_html = page_html.replace("_BODY_", body_html)
                    page_html = page_html.replace("_TITLE_", label)
                    f.write(page_html)
            except KeyError:
                print(f"Function {function_name} not found.")

def pokemonTypesList():     # this function finds all the types and adds them to navbar but does not make the pages
    global nav_items
    typesList = []
    headers = myFileList[0]
    type1_col = headers.index("Type 1")
    type2_col = headers.index("Type 2")
    for row in myFileList[1:]:
        if row[type1_col] != "" and row[type1_col] not in typesList:
            typesList.append(row[type1_col])
        if row[type2_col] != "" and row[type2_col] not in typesList:
            typesList.append(row[type2_col])

    typesList = sorted(typesList)  # makes my types alphabetical on navbar

    for item in nav_items:
        if item[0] == "Types":
            item.append([])  # Add submenu list as its own list becuase its gonna contain lists
            for type in typesList:
                item[2].append([type, f"HTML/{type.lower()}.html"])  # the "2" is used to represent the third index where we are adding the list of types

    return typesList
    
def pokemonTypesPage(): # makes the actual pages for pokemon types
    typesList = pokemonTypesList()
    headers = myFileList[0]
    type1_col = headers.index("Type 1")
    type2_col = headers.index("Type 2")
    
    for type in typesList:
        indexes = []
        i = 1  # Start at 1 to skip the header row
        while i < len(myFileList):
            row = myFileList[i]
            if (row[type1_col] == type or row[type2_col] == type):   # checks if either type of the pokemon is the type for the page
                indexes.append(i)
            i += 1

        typebody = makeHeader(type,1)
        typebody += makeTable("", headers, [myFileList[i] for i in indexes])

        with open(f"HTML/{type.lower()}.html", "w") as f:
            typePage = page.replace("_NAVBAR_", makeNavbar(nav_items,1))
            typePage = typePage.replace("_BODY_", typebody)
            typePage = typePage.replace("_STYLE_", '<link href="../CSS/PokeStyle.css" rel="stylesheet" type="text/css">')
            typePage = typePage.replace("_TITLE_", type)
            f.write(typePage)
    

pokemonTypesPage() # ran to make all the type pages, i do it inside the function since it requires a for loop
# pokemonTypesList() is ran inside the pokemonTypesPage() page, so it already updates the nav items, don't need to run on it's own


makeTop10andAllPages()  # generate the Top10 and All Pokemon pages

homepage = page.replace("_STYLE_", '<link href="CSS/PokeStyle.css" rel="stylesheet" type="text/css">')
homepage = homepage.replace("_NAVBAR_", makeNavbar(nav_items, 0))
homepage = homepage.replace("_BODY_", makeHomeBody())
homepage = homepage.replace("_TITLE_", "Pokedex Home")
print(homepage)



