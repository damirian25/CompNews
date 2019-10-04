# Исхаков Дамир
# Курсовая работа: news.mail.ru

from lxml import etree
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

if __name__ == "__main__":
    url = "https://news.mail.ru/society/"

    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    
    driver.get(url)
    while len(driver.find_element_by_class_name("paging__content")\
              .find_elements_by_class_name("newsitem")) < 1000:
        moreNewsElem = driver.find_element_by_class_name("paging")\
                       .find_element_by_class_name("paging__more")\
                       .find_element_by_tag_name("button")
        moreNewsElem.click()
        time.sleep(1)
    
    news = []
    for newsElem in driver.find_element_by_class_name("paging__content")\
        .find_elements_by_class_name("newsitem"):
        news.append(newsElem.find_element_by_tag_name("a")\
                    .get_attribute("href"))
    
    index = 0
    while index < len(news):
        driver.get(news[index])
        index = index + 1

        newsTitle = driver.find_element_by_class_name("hdr_collapse")\
                    .find_element_by_class_name("hdr__inner").text
        
        newsText = driver.find_element_by_class_name("article__intro").text
        otherTextElems = driver.find_element_by_class_name("article__text")\
                         .find_elements_by_class_name("article__item_html")
        for otherTextElem in otherTextElems:
            newsText = newsText + "\n" + otherTextElem.text
    
        xmlData = etree.Element("doc")

        sourceXmlData = etree.SubElement(xmlData, "source")
        sourceXmlData.text = etree.CDATA(driver.current_url)

        categoryXmlData = etree.SubElement(xmlData, "category")
        categoryXmlData.text = etree.CDATA("Общество")
        categoryXmlData.attrib['verify'] = "true"
        categoryXmlData.attrib['type'] = "str"
        categoryXmlData.attrib['auto'] = "true"
    
        titleXmlData = etree.SubElement(xmlData, "title")
        titleXmlData.text = etree.CDATA(newsTitle)
        titleXmlData.attrib['verify'] = "true"
        titleXmlData.attrib['type'] = "str"
        titleXmlData.attrib['auto'] = "true"

        textXmlData = etree.SubElement(xmlData, "text")
        textXmlData.text = etree.CDATA(newsText)
        textXmlData.attrib['verify'] = "true"
        textXmlData.attrib['type'] = "str"
        textXmlData.attrib['auto'] = "true"
    
        xmlTree = etree.ElementTree(xmlData)
        xmlTree.write("mailrunews\\news " + str(index) + ".xml",\
                      encoding="utf-8", xml_declaration=True,\
                      pretty_print=True)
        
    driver.close()
