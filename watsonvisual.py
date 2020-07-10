import csv
import json
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(
    '[version]',
    iam_apikey='[api key]')



#------- HERE BE COLOR VALUE RETURNER-------#
def mondoImageParse(imageURL):
    classes_result = visual_recognition.classify(url=imageURL).get_result()
    classez = extract_values(classes_result, 'class')
    score = extract_values(classes_result, 'score')
    schema_dict = dict(zip(classez, score))

    for k, v in sorted(schema_dict.items(), key=by_value, reverse=True):
        if "color" in k:
         return k


#------- HERE BE JSON KEY EXTRACTION-------#
def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

#-------HERE BE DICTIONARY SORTING-------#
def by_value(item):
    return item[1]

#-------HERE BE CSV READER-------#
input_file = csv.DictReader(open("dummytest.csv"))

#-------HERE BE MAIN-------#

with open('eggs3thereckoning.csv', 'w', newline='') as csvfile:
    colorwriter = csv.writer(csvfile, delimiter=',',
                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in input_file:
        sku = row["sku"]
        url = row["url"]
        color = str(mondoImageParse(url))

        colorwriter.writerow([sku]+[url]+[color])
