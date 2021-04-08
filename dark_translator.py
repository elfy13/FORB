from bs4 import BeautifulSoup
import urllib
import requests
import re

plainFile = "cube_list.txt"
xmlFile = "yugioh_cube.xml"
forbiddenURL = "https://db.ygoprodeck.com/card/?search="

def prolog(fd):
    prologString = '''<?xml version="1.0" encoding="UTF-8"?>
    <cockatrice_carddatabase version="4">
        <sets>
            <set>
                <name>FOR</name>
                <longname>The forbidden set</longname>
                <settype>Custom</settype>
                <releasedate>2021-03-23</releasedate>
            </set>
        </sets>

        <cards> '''
    fd.write(prologString)
    return 0

def cardParser(fd):
    inputFile = open(plainFile, "r")
    lines = inputFile.readlines()
    for line in lines:
        if not line.startswith("--") and not(line == '\n'):
            line = line.rstrip('\n')
            print("Adding: " + line)
            
            print("Single Card URL")
            # Request.get has to have '&' character escaped
            singleCardURL = forbiddenURL + line.replace('&', '%26')
            markup = requests.get(singleCardURL, "html.parser")
            print(singleCardURL)
            
            soup = BeautifulSoup(markup.text, features="lxml")
            
            print("Picture URL")
            pictureString = soup.find('meta', {'property' : 'og:image:secure_url'}).get('content')
            print(pictureString)
            
            print("Text String")
            textString = soup.find('meta', {'property' : 'og:description'}).get('content')
            print(textString)
            
            print("Alternate name")
            reSearchQuery = re.search('[0-9]+', pictureString)
            altName = reSearchQuery.group(0)
            print(altName + '\n')

            # XML also has the same issue
            xmlSafeName = "yugiohset_" + line.replace('&', '&amp;').replace('"', '&quot;').replace('\'', '&apos;').replace('<', '&lt;').replace('>', '&gt;')
            xmlSafeText = textString.replace('&', '&amp;').replace('"', '&quot;').replace('\'', '&apos;').replace('<', '&lt;').replace('>', '&gt;')

            cardXML = '''
            <card>
            <name>''' + xmlSafeName + '''</name>
            <text>''' + xmlSafeText + '''</text>
            
            <prop>
                <layout>normal</layout>
                <side>front</side>
                <type>Creature</type>
                <maintype>Creature</maintype>
                <manacost>R</manacost>
                <cmc>0</cmc>
                <colors>W</colors>
                <coloridentity>W</coloridentity>
                <pt>1/1</pt>
                <loyalty>0</loyalty>
                <format-standard>legal</format-standard>
                <format-commander>legal</format-commander>
                <format-modern>legal</format-modern>
                <format-pauper>legal</format-pauper>
            </prop>
            <set rarity="common" uuid="12345678-abcd-1234-abcd-1234567890ab" num="42" muid="123456" picurl="''' + pictureString + '''">FOR</set>
            <related>''' + altName + '''</related>
            <reverse-related>Another card name</reverse-related>
            <token>1</token>
            <tablerow>2</tablerow>
            <cipt>1</cipt>
            <upsidedown>1</upsidedown>
            </card>
            '''
            fd.write(cardXML)
    return 0

def epilogue(fd):
    epilogueString = '''
        </cards>
    </cockatrice_carddatabase>
    '''
    fd.write(epilogueString)
    return 0

def main():
    print("Dark Translator")
    openFile = open(xmlFile, "w")
    prolog(openFile)
    cardParser(openFile)
    epilogue(openFile)
    openFile.close()

if __name__== "__main__":
    main()
