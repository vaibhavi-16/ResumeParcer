from django.shortcuts import render
from django.shortcuts import render,redirect
import requests
from .models import *

# Create your views here.

import docx2txt
import PyPDF2
import re
import nltk
from nltk.corpus import stopwords
from nltk.corpus import stopwords
nltk.download('stopwords')
stop = stopwords.words('english')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
import spacy
import en_core_web_sm
from spacy.matcher import Matcher
import re
# from nltk.corpus import stopwords
import pandas as pd
import spacy
from pdfminer.high_level import extract_text
# from django.core.files.storage import FileSystemStorage




def doctotext(m):
    temp = docx2txt.process(m)
    if temp:
        return temp.replace('\t', ' ')
    return None

def pdftotext(m):
  return extract_text(m)


# load pre-trained model
nlp = en_core_web_sm.load()

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)


def extract_name(resume_text):
    nlp_text = nlp(resume_text)
    
    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    
    matcher.add('NAME', [pattern])
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text

def extract_mobile_number(resume_text):
    PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
    phone = re.findall(PHONE_REG, resume_text)
 
    if phone:
        number = ''.join(phone[0])
 
        if resume_text.find(number) >= 0 and len(number) < 16:
            return number
    return None

def extract_emails(resume_text):
    EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
    mail =  re.findall(EMAIL_REG, resume_text)
    return mail[0]

STOPWORDS = set(stopwords.words('english'))

# Education Degrees
EDUCATION = [
            'BE','B.E.', 'B.E', 'BS', 'B.S', 'B.Tech', 'BTech', 'BTECH', 'B.TECH'
            'ME', 'M.E', 'M.E.', 'M.B.A', 'MBA', 'MS', 'M.S', 
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
            'SSLC', 'SSC' 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
        ]
def extract_education(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.text.strip() for sent in nlp_text.sents]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]
    
    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(r'(((20|19)(\d{})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return education[0]

def extract_skills(resume_text):
    # nlp_text = nlp(resume_text)
    nlp = spacy.load('en_core_web_sm')
    nlp_text = nlp(resume_text)
    noun_chunks = nlp_text.noun_chunks
    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]
    # colnames = ['skill']
  
    skills = [
    'machine learning',
    'data science',
    'Python',
    'word',
    'excel',
    'English',
    'html',
    "CSS",'JavaScript',
    'java','Core Java',
    'MySQL','SQL','Bootstrap','Django','Django Framework'
]
 
    skillset = []
   
    for token in tokens:
        if token in skills:
            skillset.append(token)
   
    for token in noun_chunks:
        token = token.text.strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i for i in skillset])]

# if __name__ == '__main__': 
  
    # FilePath = r'C:\Users\Dell\Downloads\DeepaksResume.pdf'
    # # FilePath.lower().endswith(('.docx'))
    # # if FilePath.endswith('.docx'):
    # #   textinput = doctotext(FilePath) 
    # #   print('Name: ',extract_name(textinput))
    # #   print('Mobile Number: ',extract_mobile_number(textinput))
    # #   print('Mail id: ',extract_emails(textinput))
    # #   print('Qualification: ',extract_education(textinput))
    # #   print ('Skills: ',extract_skills(textinput))
    # if FilePath.endswith('.pdf'):
    #   textinput = pdftotext(FilePath)
    #   print('Name: ',extract_name(textinput))
    #   print('Mobile Number: ',extract_mobile_number(textinput))
    #   print('Mail id: ',extract_emails(textinput))
    #   print('Qualification: ',extract_education(textinput))
    #   print ('Skills: ',extract_skills(textinput))

    # else:
    #   print("File not support")



def home(request):
    if request.method == 'POST':
        # myfile = request.FILES['myfile'].read()
        myfile = request.POST.get('myfile')
        # myfile = request.FILES['myfile']
        # fs = FileSystemStorage()
        # filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        name = ""
        num = ""
        mail = ""
        quali = ""
        skill = []
        if ' ' in myfile:
            myfile.replace(' ','')
        # myfile.replace("'",'')
        # print(myfile,"MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
        # if myfile.endswith('.pdf'):
        textinput = pdftotext(myfile)
        name += extract_name(textinput)
        num += extract_mobile_number(textinput)
        mail += extract_emails(textinput)
        quali += extract_education(textinput)
        skill += extract_skills(textinput)
        
        context = {
            'id':1,
            'x':4,
            'name':name,
            'num':num,
            'mail':mail,
            'quali':quali,
            'skill':skill,
        }
        return render(request,'project/index.html', context)
    else:
        return render(request,'project/index.html')

def about(request):
    # username = 'Deepak@1234'
    # name = StudentForm.objects.get(user = username)
    return render(request,'project/about.html')





