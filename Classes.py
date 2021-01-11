class Webshop:
    def __init__(self, url, name, category):
        self.url = url
        self.name = name
        self.category = category


class Test:
    def __init__(self, url, name, category, test):
        self.url = url
        self.name = name
        self.category = category
        self.test = test


class Categorycount:
    def __init__(self, categoryname, count):
        self.categoryname = categoryname
        self.count = count


class CMScount:
    def __init__(self, cms, count):
        self.cms = cms
        self.count = count

