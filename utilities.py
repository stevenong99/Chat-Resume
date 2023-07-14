import openai

def is_api_key_valid(api_key):
    try:
        openai.api_key = api_key
        response = openai.Completion.create(
            engine="davinci",
            prompt="This is a test.",
            max_tokens=5
        )
    except:
        return False
    else:
        return True