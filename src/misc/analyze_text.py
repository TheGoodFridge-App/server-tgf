import os, io
from google.cloud import vision
from google.cloud import language_v1
from google.cloud.language_v1 import enums

# This code is required for Python 2.7
try: input = raw_input
except NameError: pass

# Authenticating the code of google vision API with credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials.json"
client = vision.ImageAnnotatorClient()

path = './images/image4.jpeg'
document_text = ""

def PictureToText():

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation
    output_file = open("./output_text.txt","w")

    global document_text
    document_text = str(document.text.encode(encoding='UTF-8'))

    print("Reading image done")

    output_file.write(document_text)
    output_file.close()


def sample_analyze_entities():
    """
    Analyzing Entities in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()
    
    text_content = document_text
   
    # Available types: PLAIN_TEXT, HTML
    type_ = enums.Document.Type.HTML

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_entities(document, encoding_type=encoding_type)
    # Loop through entitites returned from the API
    for entity in response.entities:
        print(u"Representative name for the entity: {}".format(entity.name))
        # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
        # Get the salience score associated with the entity in the [0, 1.0] range
        print(u"Salience score: {}".format(entity.salience))
        # Loop over the metadata associated with entity. For many known entities,
        # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
        # Some entity types may have additional metadata, e.g. ADDRESS entities
        # may have metadata for the address street_name, postal_code, et al.
        for metadata_name, metadata_value in entity.metadata.items():
            print(u"{}: {}".format(metadata_name, metadata_value))

        # Loop over the mentions of this entity in the input document.
        # The API currently supports proper noun mentions.
        for mention in entity.mentions:
            print(u"Mention text: {}".format(mention.text.content))
            # Get the mention type, e.g. PROPER for proper noun
            print(
                u"Mention type: {}".format(enums.EntityMention.Type(mention.type).name)
            )

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))



if __name__ == '__main__':
    PictureToText()
    sample_analyze_entities()