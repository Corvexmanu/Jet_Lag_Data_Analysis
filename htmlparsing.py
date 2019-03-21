# 
# Example file for parsing and processing HTML
#

# import the HTMLParser module
# in Python 3 you need to import from html.parser
from html.parser import HTMLParser

metacount = 0;

# create a subclass of HTMLParser and override the handler methods
class MyHTMLParser(HTMLParser):

  # function to handle character and text data (tag contents)
  def handle_data(self, data):
    if (data.isspace() or len(data)<3 or data.count(")") != 0):
      return
    print ("Encountered some text data:", data)

  
def main():
  # instantiate the parser and feed it some HTML
  parser = MyHTMLParser()
    
  # open the sample HTML file and read it
  f = open("usazones.html")
  if f.mode == "r":
    contents = f.read() # read the entire file
    parser.feed(contents)
  
  print ("%d meta tags encountered" % metacount)

if __name__ == "__main__":
  main();
  