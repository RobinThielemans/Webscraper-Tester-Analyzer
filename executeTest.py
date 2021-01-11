import csv
import os
from datetime import datetime
from Classes import Webshop, Test, Categorycount
import glob


# PRINT CATEGORY FUNCTION
def printcategorylist():
    print("(Categories in Dutch)")
    print("\nCategorie \t\t\t\tAantal winkels")
    print("--------------------\t---------------\n\n")

    for category in categories:
        if foundcategories.count(category) > 0:
            categoriecounts.append(Categorycount(category, foundcategories.count(category)))
            if len(category) < 8:
                print(category + "\t\t\t\t\t" + str(foundcategories.count(category)))
            elif len(category) < 12:
                print(category + "\t\t\t\t" + str(foundcategories.count(category)))
            elif len(category) < 16:
                print(category + "\t\t\t" + str(foundcategories.count(category)))
            elif len(category) >= 16:
                print(category + "\t\t" + str(foundcategories.count(category)))

#INITS
webshoplist = []
webshoptestlist = []
categories = ["Voeding", "Drank", "Herenmode", "Damesmode", "Mode", "koken", "Koken", "Vrije Tijd", "Fotografie",
              "Alcoholische drank", "Sport", "Reizen", "Make-up", "Verzorging",
              "Muziek", "Tuin", "Dier", "Klussen", "Schoenen", "Juwelen", "Baby", "Kind", "Speelgoed",
              "Kinderkledij", "Kantoor", "Computer", "Elektronica", "Multimedia", "Wonen", "Huishouden",
              "Gadgets", "Inspiratie", "Bloemen", "Bril", "Lenzen", "Stoffen", "Verlichting",
              "Lingerie", "Mooi", "Gezond", "Cadeau", "Accessoires", "Design", "Ambacht", "Kunst",
              "Tapijten", "Gereedschap", "Elektro", "Kranten", "Tijdschriften", "Elektro", "Wenskaarten",
              "Wenskaarten", "Cultuur", "Naaien", "Breien", "Meubels", "Woonaccessoires", "Bouwmaterialen",
              "Gereedschap", "Warme dranken", "Pharma", "Boeken", "Strips", "Textiel", "Auto", "Geboortekaartjes",
              "Stationary", "Kamperen", "Stickers", "Verf", "Behang", "Inktpatronen", "Telefonie", "Sanitair",
              "Lifestyle", "Badmode", "Shapewear", "Nachtkledij", "Afsluitingen", "Gezelschapsspellen", "Podiumkunsten"]
categories.sort()
foundcategories = []
categoriecounts = []
usercategories = []
testednames = []


# CUSTOM FILE PATHS
print("Do you want to use the default file included in this git? Or do you want to test on a Custom file?\n"
      "Press enter for default or press n for custom")
custom = input()
if custom == "n":
    csvfiles = glob.glob("csv_files/webscraped_webshops/*.csv")
    print("\n")
    for filenr, file in enumerate(csvfiles):
        print(str(filenr) + ": " + str(file))
    print("Type the number of the file u wish to test on")
    filenr= int(input())
else:
    csvfiles = ["csv_files/webscraped_webshops/Allwebshops_11_01_2021.csv"]
    filenr = 0


# OPEN FILE AND WRITE INTO LIST
with open(csvfiles[filenr], 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        webshoplist.append(Webshop(row[0], row[1], row[2:]))

# WRITE ALL CATEGORIES TO LIST
for webshop in webshoplist:
    for category in categories:
        if webshop.category[0].find(category) >= 0:
            foundcategories.append(category)

# ASK WHICH COMMAND
print('Which test do you want to execute? (Syntax: this input + " scripturl " + suffix(next input)(no space for url)')
testname = input()
print('Which suffix?(optional, don\'t start with space") (Syntax: first input + " scripturl " + this input)')
suffix = input()

# ASK WHICH CATEGORY
print("Do you want to test specific categories (j/n)")
cat = input()

# GET CATEGORIES
if cat == "j":
    firstrun = True
    while True:
        if not firstrun:
            print("Do you want to test an extra category?(j/n)")
            inextra = input()
        else:
            inextra = "j"
            firstrun = False
        if inextra == "n":
            break
        elif inextra == "j":
            printcategorylist()
            print("\nChoose a category out of the list above to test on and type it underneath")
            inusercategory = input()
            usercategories.append(inusercategory)
        else:
            print("U have spelled the category wrong")

# CHECK WHICH WEBSHOPS TO TEST WITH CATEGORY
webshopstotest = []
for x in webshoplist:
    for usercategory in usercategories:
        if x.category[0].find(usercategory) >= 0 and x.name not in webshopstotest:
            webshopstotest.append(x.name)

# TEST WEBSHOPS
for x in webshoplist:
    if x.name != "url":
        if cat == 'j':
            for webshoptotest in webshopstotest:
                if x.name.find(webshoptotest) >= 0 and x.name not in testednames:
                    test = os.popen(testname + " " + x.url + " " + suffix).read()
                    print("Naam: " + x.name)
                    print("Winkelcategorie: " + x.category[0])
                    print("WatwebTest: " + test)
                    webshoptest = Test(x.url, x.name, x.category, test)
                    webshoptestlist.append(webshoptest)
                    testednames.append(x.name)
                    print("TESTED " + str(len(testednames)) + " OUT OF " + str(len(webshopstotest)) + " WEBSHOPS")
        else:
            test = os.popen(testname + " " + x.url + " " + suffix).read()
            print("Naam: " + x.name)
            print("Winkelcategorie: " + x.category[0])
            print("WatwebTest: " + test)
            webshoptest = Test(x.url, x.name, x.category, test)
            webshoptestlist.append(webshoptest)
            testednames.append(x.name)
            print("TESTED " + str(len(testednames)) + " OUT OF " + str(len(webshoplist)) + " WEBSHOPS")

    elif x.name == "url":
        print("SCAN STARTED")

# GET TIME FOR FILENAMESTRING
now = datetime.now()
now = str(now).replace(" ","_")
now = now[:len(now)-10]

# WRITE FILENAMESTRING
if usercategories:
    usercategoriesstr = "_".join(usercategories)
    csvfilename = "csv_files/tested_webshops/" + testname + "test" + "_" + usercategoriesstr + "_winkels" + "_" + str(now) + ".csv"
else:
    csvfilename = "csv_files/tested_webshops/" + testname + "test" + str(now) + ".csv"

# WRITE TO CSV
with open(csvfilename, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['naam', 'url', 'categorie'])
    for webshoptest in webshoptestlist:
        writer.writerow([webshoptest.name, webshoptest.url, webshoptest.category, webshoptest.test])
print("\nYour file: " + csvfilename + " has been created")
