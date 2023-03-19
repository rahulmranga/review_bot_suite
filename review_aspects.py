from transformers import AutoTokenizer, AutoModelForSequenceClassification
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from collections import defaultdict
import torch.nn.functional as F
import torch

tokenizer = AutoTokenizer.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")
model = AutoModelForSequenceClassification.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")
nlp = spacy.load("en_core_web_md")


attributes = {
    "food": ["food", "cuisine", "dish", "flavor","fresh"],
    "service": ["service", "waitstaff", "server", "staff","manager"],
    "ambiance": ["ambiance", "atmosphere", "decor", "music","place","seat"],
    "value": ["value", "price", "cost", "affordability"],
    "location": ["nearby", "address", "parking", "accessibility","locality","neighbourhood"]
}



def get_similar_attribute(word, threshold=0.5):
        max_similarity = 0
        most_similar_attribute = None

        for attribute, attribute_words in attributes.items():
            for attribute_word in attribute_words:
                similarity = nlp(word).similarity(nlp(attribute_word))
                if similarity >= threshold and similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_attribute = attribute_word
        return most_similar_attribute

def get_summary(text, num_sentences=2):
    doc = nlp(text.lower())
    sentences = [str(sent).strip() for sent in doc.sents]
    word_frequencies = defaultdict(float)
    for word in doc:
        if word.text not in STOP_WORDS:
            word_frequencies[word.text] += 1
    max_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] /= max_frequency
    sentence_scores = defaultdict(float)
    
    for sent in sentences:
        for word in nlp(sent):
            if word.text in word_frequencies.keys():
                sentence_scores[sent] += word_frequencies[word.text]
    top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
    
    summary = [sentence[0] for sentence in top_sentences]
    
    return ' '.join(summary)

def get_topics(review_text):
    summary_text = get_summary(review_text)
    mentioned_attributes = set()
    for word in summary_text.split():
        attribute = get_similar_attribute(word)
        if attribute is not None:
            mentioned_attributes.add(attribute)

    return mentioned_attributes


def get_sentiments(sentence,attrs):
#sentence = restaurants['text'][0]
# print(f"Sentence: {sentence}")
# print()
    attrs=attrs.split(' | ')
    result={}
    for i in attrs:
        aspect = i
        inputs = tokenizer(f"[CLS] {sentence} [SEP] {aspect} [SEP]",return_tensors="pt")
        outputs = model(**inputs)
        res=F.softmax(outputs.logits, dim=1).detach()[0]
        if(torch.argmax(res).item()==0):
            Sent="Negative"
        elif(torch.argmax(res).item()==1):
            Sent="Neutral"
        else:
            Sent="Positive"
        result[i]={Sent:max(res).item()}
    return result