import secrets
import string


from Context import get_application_specific_schema, get_application_specific_context, get_generic_context


def setup_connection(product_code):
    product_exists = verify_product_code_exists(product_code)
    if product_exists:
        token = generate_token()
        return {"status_code": 200, "token": token, "context": get_full_context(product_code)}
    return {"status_code": 404, "token": ""}


def verify_product_code_exists(product_code):
    products_code_list = get_product_codes_list()
    print(products_code_list)
    return product_code.lower() in (code.lower() for code in products_code_list)


def get_product_codes_list():
    products_list = []
    with open('ProductsList.txt', 'r') as file:
        for line in file:
            product_code = line.rstrip('\n')
            products_list.append(product_code)
    return products_list


def get_full_context(product_code):
    app_schema = get_application_specific_schema(product_code)
    app_context = get_application_specific_context(product_code)
    generic_context = get_generic_context()

    full_context = {'app_schema': app_schema, 'app_context': app_context, 'generic_context': generic_context}
    return full_context


def get_context_var(token, user_context):
    context_vars = user_context.get()
    return context_vars[token]


def generate_token(length=32):
    characters = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(characters) for _ in range(length))
    return token