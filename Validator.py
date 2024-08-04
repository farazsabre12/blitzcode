def validate(response):
    print('Validating response...')
    if response.isValid:
        return response.Response
    else:
        return response.FailureReason