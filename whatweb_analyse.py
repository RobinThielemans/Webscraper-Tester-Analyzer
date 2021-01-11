import csv
from Classes import Test, CMScount
import matplotlib.pyplot as plt
import glob
from datetime import datetime



# SORTLISTFUNCTION
def sort_list(list1, list2):
    zipped_pairs = zip(list2, list1)
    z = [x for _, x in sorted(zipped_pairs)]
    return z


#  FORMAT CHART DATA FUNCTION
def my_fmt(x):
    return '{:.2f}%({:.0f})'.format(x, cmsnrtotal*x/100)


#  FORMAT CHART DATA FUNCTION
def my_fmt_nocms(x):
    return '{:.2f}%({:.0f})'.format(x, cmsnrtotalWithNoCMS*x/100)


webshoptestlist = []

errors = ["500 Internal Server Error", "403 Forbidden"]
errorsites = []
erroramount = []

cmsnames = ["WordPress", "Joomla", "Drupal", "Prestashop", "Sitecore", "Shopify",
            "SquareSpace", "Magento", "Wix", "JouwWeb", "CPanel", "WebNode", "Plesk", "One.com",
            "Bitrix", "Blogger", "OpenCart", "Weebly", "TYPO3", "Bigcommerce", "Webflow",
            "Adobe Dreamweaver", "GoDaddy", "Tilda", "DataLife Engine", "Prom.ua", "Gatsby",
            "FrontPage", "HubSpot CMS", "DotNetNuke", "GitHub Pages", "Duda", "Craft CMS",
            "Adobe Muse", "XenForo", "vBulletin", "phpBB", "ExpressionEngine", "Dealer.com",
            "CMS.S3", "Sitecore CMS", "Hugo", "MODx", "uCoz", "Shopware", "nopCommerce",
            "Concrete5", "CS-Cart", "Discuz!", "Cafe24", "October CMS", "Kentico", "IPS Community Suite",
            "Progress Sitefinity", "SharePoint", "MediaWiki", "Jimdo", "Mobirise", "Ticimax", "Liferay",
            "Adobe Experience Manager", "Volusion", "Jekyll", "Ghost", "osCommerce", "Contao", "Simple Machines Forum",
            "SilverStripe", "UMI.CMS", "Zen Cart", "Yardi", "Salesforce Commerce Cloud", "NetCat", "Moodle",
            "SPIP", "ProcessWire", "Lightspeed eCom", "Odoo", "CivicEngage", "BentoBox", "WebSite x5",
            "Business Catalyst", "HostCMS", "VTEX", "InstanCMS", "3dcart", "Blackboard", "Tumblr", "CDK Global",
            "Microsoft Word", "Google Sites", "EC-Cube", "JTL-Shop", "RapidWeaver", "CMS Made Simple",
            "Plone", "JustSystems Homepage Builder", "1&1 IONOS MyWebsite", "ePages", "CM4All", "PagesJaunes",
            "DudaMobile", "Contao", "NextCloud", "Strato Sitebuilder"]

cmsfound = []
cmsusedWithNoCMS = []
cmsnrWithNoCMS = []
cmsused = []
cmsnr = []
cmsrest = 0
cmsrestNoCMS = 0
cmsCount = []

# CUSTOM FILE PATHS
print("Do you want to use the default file included in this git? Or do you want to test on a Custom file?\n"
      "Press enter for default or press n for custom")
custom = input()
if custom == "n":
    csvfiles = glob.glob("csv_files/tested_webshops/*.csv")
    print("\n")
    for filenr, file in enumerate(csvfiles):
        print(str(filenr) + ": " + str(file))
    print("Type the number of the file u wish to test on")
    filenr= int(input())
else:
    csvfiles = ["csv_files/tested_webshops/default_allwebsites_whatweb_-v.csv"]
    filenr = 0


# OPEN CSV FILE AND WRITE INTO LIST
with open(csvfiles[filenr], 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        webshoptestlist.append(Test(row[1], row[0], row[2], row[3:]))

# FIND ERRORS AND CMS AND WRITE TO LISTS
for webshoptest in webshoptestlist:
    for error in errors:
        if str(webshoptest.test).find(error) >= 0:
            errorsites.append(webshoptest.name)
            erroramount.append(error)
    for cms in cmsnames:
        if str(webshoptest.test).find(cms) >= 0:
            cmsfound.append(cms)

noerrorammount = (len(webshoptestlist) - len(errorsites))
nocmsammount = (len(webshoptestlist) - len(cmsfound))

# PRINT ERROR
print("-------------------")
print("Errors")
print("-------------------")
for error in errors:
    print(error + ": " + str(erroramount.count(error)))

# PRINT CMS
print("Websites zonder errors: " + str(noerrorammount))
print("-------------------")
print("CMS")
print("-------------------")


# CUTOFF FOR OTHER IN CHART
cutoffNoCMS = round(len(cmsfound)/25)
cutoff = round(len(cmsfound)/150)

# WRITE CMS INTO LISTS AND PRINT CMS
for cms in cmsnames:
    print(str(cms) + ": " + str(cmsfound.count(cms)))
    if cmsfound.count(cms) > 0:
        cmsCount.append(CMScount(cms, cmsfound.count(cms)))
    if cmsfound.count(cms) >= cutoff and cmsfound.count(cms) > 0:
        cmsused.append(cms)
        cmsnr.append(cmsfound.count(cms))
    if cmsfound.count(cms) >= cutoffNoCMS:
        cmsusedWithNoCMS.append(cms)
        cmsnrWithNoCMS.append(cmsfound.count(cms))
    if cutoff > cmsfound.count(cms) > 0:
        cmsrest += cmsfound.count(cms)
    if cutoffNoCMS > cmsfound.count(cms) > 0:
        cmsrestNoCMS += cmsfound.count(cms)

print("Geen CMS gedetecteerd: " + str(nocmsammount))

# FIX DATA FOR CHARTS
cmsusedsorted = sort_list(cmsused, cmsnr)
cmsnr.sort()
if cmsrest > 0:
    cmsusedsorted.insert(0, "Andere")
    cmsnr.insert(0, cmsrest)


# TOTAL CMS
cmsnrtotal = 0
for cms in cmsnr:
    cmsnrtotal += cms
print("Totaal CMSgebruikers: " + str(cmsnrtotal))

# PERCENTAGE CALCULATION
sizespercentages = []
sizesandpercentages = []
for cms in cmsnr:
    sizespercentages.append(cms/cmsnrtotal * 100)
    sizesandpercentages.append(str(round((cms/cmsnrtotal * 100), 2)) + "% (" + str(cms) + ")")

# DATA FOR PIECHART
labels = cmsusedsorted
sizes = cmsnr
listlength = len(labels)

# REVERSE LABELS FOR LEGEND
labelsreverse = []
sizesandpercentagesreverse = []
for label in labels:
    labelsreverse.append(label)
for sizesandpercentage in sizesandpercentages:
    sizesandpercentagesreverse.append(sizesandpercentage)
labelsreverse.reverse()
sizes.reverse()
sizesandpercentagesreverse.reverse()

# EXPLODES FOR CHARTS
myexplode = []
smallnrexplode = 0.25
for nr in sizes:
    if nr <= round(len(cmsfound) / 50) > round(len(cmsfound) / 75):
        myexplode.append(0.3)
    elif nr <= round(len(cmsfound) / 75) > round(len(cmsfound) / 100):
        myexplode.append(0.35)
    elif nr <= round(len(cmsfound) / 100) > round(len(cmsfound) / 500):
        myexplode.append(0.4)
    elif nr == 1:
        myexplode.append(smallnrexplode)
        # smallnrexplode += 0.2
    else:
        myexplode.append(0)

# MAKE CHART WITH ONLY CMS
figure = plt.gcf() # get current figure
figure.set_size_inches(16, 9)
plt.pie(sizes, labels=labelsreverse, autopct=my_fmt, explode=myexplode, startangle=30)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.legend(loc='upper left', labels=['%s, %s' % (l, s) for l, s in zip(labelsreverse, sizesandpercentagesreverse)])
# plt.show()
# plt.close()
print("Give a filename to save the graph with all different CMS as (dont add file extension to name)")
filename = input()
fullfilename = "Piecharts/" + filename + ".png"
plt.savefig(fullfilename, dpi=100)
plt.close()
print("\nYour PieChart: " + fullfilename + " has been created")

# FIX DATA FOR CHARTS
cmsusedWithNoCMS.append("No CMS detected")
cmsnrWithNoCMS.append(nocmsammount)
cmsusedWithNoCMSSorted = sort_list(cmsusedWithNoCMS, cmsnrWithNoCMS)
cmsnrWithNoCMS.sort()
cmsusedWithNoCMSSorted.insert(0, "Andere")
cmsnrWithNoCMS.insert(0, cmsrestNoCMS)

# TOTAL CMS
cmsnrtotalWithNoCMS = 0
for cms in cmsnrWithNoCMS:
    cmsnrtotalWithNoCMS += cms

# PERCENTAGE CALCULATION
sizespercentagesWithNoCMS = []
sizesandpercentagesWithNoCMS = []
for cms in cmsnrWithNoCMS:
    sizespercentagesWithNoCMS.append(cms/cmsnrtotalWithNoCMS * 100)
    sizesandpercentagesWithNoCMS.append(str(round((cms/cmsnrtotalWithNoCMS * 100), 2)) + "% (" + str(cms) + ")")

# DATA FOR PIECHART
labels = cmsusedWithNoCMSSorted
sizes = cmsnrWithNoCMS
listlength = len(labels)

# REVERSE LABELS FOR LEGEND
labelsreverseWithNoCMS = []
sizesandpercentagesreverseWithNoCMS = []
for label in labels:
    labelsreverseWithNoCMS.append(label)
for sizesandpercentage in sizesandpercentagesWithNoCMS:
    sizesandpercentagesreverseWithNoCMS.append(sizesandpercentage)
labelsreverseWithNoCMS.reverse()
sizes.reverse()
sizesandpercentagesreverseWithNoCMS.reverse()

# EXPLODES
myexplode = []
smallnrexplode = 0.35
for nr in cmsnrWithNoCMS:
    if nr == 5:
        myexplode.append(0.05)
    elif nr == 4:
        myexplode.append(0.1)
    elif nr == 3:
        myexplode.append(0.2)
    elif nr == 2:
        myexplode.append(0.3)
    # elif nr == 1:
    #     myexplode.append(smallnrexplode)
    #     smallnrexplode += 0.2
    else:
        myexplode.append(0)

# CREATE PIECHART WITH NO CMS
figure = plt.gcf()
figure.set_size_inches(16, 9)
plt.pie(sizes, labels=labelsreverseWithNoCMS, autopct=my_fmt_nocms, explode=myexplode, startangle=240)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.legend(loc='upper left', labels=['%s, %s' % (l, s) for l, s in zip(
    labelsreverseWithNoCMS, sizesandpercentagesreverseWithNoCMS)])
# plt.show()
# plt.close()
print("Give a filename to save this graph with all Non-CMS too as (dont add file extension to name)")
filename = input()
fullfilename = "Piecharts/" + filename + ".png"
plt.savefig(fullfilename, dpi=100)
plt.close()
print("\nYour PieChart: " + fullfilename + " has been created")


# GET TIME FOR FILENAMESTRING
now = datetime.now()
now = str(now).replace(" ","_")
now = now[:len(now)-10]

# WRITE FILENAMESTRING
csvfilename = "csv_files/cms_webshops/cms_" + str(now) + ".csv"

# WRITE TO CSV
with open(csvfilename, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['cms', 'aantal'])
    for cmscountitem in cmsCount:
        writer.writerow([cmscountitem.cms, cmscountitem.count])
print("\nYour file: " + csvfilename + " has been created")
