import argparse
import json

from spire.doc import *
from spire.doc.common import *

 

# Create a Document object
def main(number):
    # print(f"sdasdasdasd: {number}")
    # string_array = ["f",f"{number}","eeff"]
    
    data = {"name":"moien","surname":"forghani"}
    
    json_output = json.dumps(data)
    print(json_output)
    
    # output_string = '/n'.join(string_array)
    # print(output_string)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('number',type=int,help='')
    args = parser.parse_args()
    main(args.number)

doc = Document()

 

# Load a Word file

doc.LoadFromFile("/Users/macbookpro/nigeb_server/media/files/ChatGPT_Commands.docx")

 

# Get text from the entire document

text = doc.GetText()

 

# Print text

# print(text)
