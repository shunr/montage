class MontageClip:

    def __str__(self):
        return "%s\n%s\n%s\n%s" % (self.title, self.author, self.link, self.src)

    def __init__(self, title, author, link, src):
        self.title = title
        self.author = author
        self.link = link
        self.src = src
