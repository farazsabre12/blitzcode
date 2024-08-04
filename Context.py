import json


def get_application_specific_schema(productCode):
    f = open(productCode + 'Schema.json')
    schema = json.load(f)
    f.close()
    return schema


def get_application_specific_context(productCode):
    with open(productCode + 'Context.txt', 'r') as file:
        context = file.read().rstrip('\n')
    with open(productCode + 'Example.txt', 'r') as file:
        example = file.read().rstrip('\n')
    return context + example


def get_generic_context():
    with open('GenericContext.txt', 'r') as file:
        context = file.read().rstrip('\n')
    return context