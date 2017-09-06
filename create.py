import sqlite3
#from _elementtree import ElementTree as ET
import xml.etree.ElementTree as ET
import sys

#CREATE DATABASE
conn = sqlite3.connect ('database.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS author')
c.execute('CREATE TABLE author (name varchar(60) PRIMARY KEY)')
c.execute("DROP TABLE IF EXISTS article")
c.execute("CREATE TABLE article(ID int PRIMARY KEY, booktitle varchar(20), title varchar(110), year int, pages varchar(20))")
c.execute("DROP TABLE IF EXISTS writes")
c.execute("CREATE TABLE writes(ID int, name varchar(60), FOREIGN KEY (name) REFERENCES author, FOREIGN KEY (ID) REFERENCES article)")
c.execute("CREATE INDEX article_ID_title_index ON article(ID, title)")
c.execute("CREATE INDEX author_name_index ON author(name)")
c.execute("CREATE INDEX writes_index ON writes(ID)")
# c.execute("CREATE UNIQUE INDEX [name] ON [author]")

conn.commit()


#parse XML
pubs = open(sys.argv[1], 'r', 0)
print "File Open!"
tree = ET.parse(pubs)
print "Parsing Done!"
root = tree.getroot()

for count in root.findall('pub'):
	ID = count.find('ID').text
	Title = count.find('title').text
	Year = count.find('year').text
	Pages = count.find('pages').text
	Booktitle = count.find('booktitle').text
			# print ID, Title, Year, Pages, Booktitlepp
	for authors in count.iter("authors"):
		for author in authors.iter("author"):
			Author = author.text
			# c.execute("IF EXISTS (SELECT * FROM author WHERE author.name != ?)", (Author,))
			c.execute("")
			c.execute("INSERT OR IGNORE INTO author VALUES (?)", (Author,))
			c.execute('INSERT INTO writes VALUES (?, ?)', (ID, Author))
			

	
	c.execute('INSERT INTO article (ID, Booktitle, Title, Year, Pages) VALUES (?, ?, ?, ?, ?)', (ID, Booktitle, Title, Year, Pages))
	print "Inserted publication: ", ID
conn.commit()
conn.close()