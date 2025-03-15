from google import genai

client =genai.Client(api_key='AIzaSyDCn5GgHhRMbziUtYzcDVMNIihorYVB-kA')

def messageGemini(message):
    """
    Basic function for sending messages to gemini api
    :param message: message to send
    :return: gemini response
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=message
    )
    return response.text