import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text="""Climate change refers to significant changes in global temperatures and weather patterns over time. While climate change is a natural phenomenon, scientific evidence shows that human activities, especially the burning of fossil fuels like coal, oil, and natural gas, have greatly accelerated the process. These activities release greenhouse gases into the atmosphere, which trap heat and cause global warming. Deforestation and industrial activities also contribute to the increase in greenhouse gas concentrations.

The consequences of climate change are far-reaching. Rising temperatures are melting polar ice caps, which causes sea levels to rise and leads to coastal flooding. Weather patterns are becoming more extreme and unpredictable, resulting in more frequent hurricanes, droughts, and wildfires. These events can devastate communities, disrupt ecosystems, and lead to loss of life and property.

Efforts to combat climate change include reducing greenhouse gas emissions, transitioning to renewable energy sources such as solar and wind, and promoting energy efficiency. Additionally, reforestation and protecting natural habitats are important steps to help absorb carbon dioxide from the atmosphere. International agreements like the Paris Agreement aim to bring countries together to take collective action on climate change."""

def summarizer(rawdocs):

    stopwords = list(STOP_WORDS)
    # print(stopwords)
    nlp=spacy.load('en_core_web_sm')
    doc=nlp(rawdocs)
    # print(doc)
    tokens=[token.text for token in doc]
    # print(tokens)
    word_freq={}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text]=1
            else:
                word_freq[word.text]+=1

    # print(word_freq)                

    max_freq=max(word_freq.values())
    # print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    # print(word_freq)    
    sent_tokens=[sent for sent in doc.sents]
    # print(sent_tokens)

    sent_scores={}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent]=word_freq[word.text]
                else:
                    sent_scores[sent]+=word_freq[word.text]
    # print(sent_scores)                    


    select_len=int(len(sent_tokens)* 0.3)
    # print(select_len)

    summary=nlargest(select_len,sent_scores,key=sent_scores.get)
    # print(summary)
    final_summary=[word.text for word in summary]
    summary=' '.join(final_summary)
    # print(text)
    # print(summary)
    # print("Length of original text ",len(text.split(' ')))
    # print("Length og summary text ",len(summary.split(' ')))

    return summary,doc, len(rawdocs.split(' ')), len(summary.split())
