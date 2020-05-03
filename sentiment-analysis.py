from google.cloud import language_v1
from google.cloud.language_v1 import enums

#text to analyze, name of product and the category it's in
def analyze(text, product_name, product_category):

    total_sentences = 0
    sentiment_score_sum = 0
    sentiment_magnitude_sum = 0
    client = language_v1.LanguageServiceClient()

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {"content": text, "type": type_}
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_sentiment(document, encoding_type=encoding_type)

    # Get overall sentiment of the input document
    print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    print(
        u"Document sentiment magnitude: {}".format(
            response.document_sentiment.magnitude
        )
    )

    # Get sentiment for each sentence in the document
    for sentence in response.sentences:
        total_sentences += 1
        sentiment_score_sum += sentence.sentiment.score
        sentiment_magnitude_sum += sentence.sentiment.magnitude
        #print(u"Sentence text: {}".format(sentence.text.content))
        #print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
        #print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))

    average_score = sentiment_score_sum/total_sentences
    average_magnitude = sentiment_magnitude_sum/total_sentences

    if __name__ == '__main__':
        analyze(text, product_name, product_category)
