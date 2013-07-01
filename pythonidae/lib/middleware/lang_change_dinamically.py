from django.utils import translation

class LangDinamicallyMiddleware(object):
    """
    This is a very simple middleware that parses a request
    and decides what translation object to install in the current
    thread context. This allows pages to be dynamically
    translated to the language the user desires (if the language
    is available, of course).
    """

    def process_request(self, request):
        try:
            language = request.COOKIES['language']
        except:
            language = translation.get_language_from_request(request)
        translation.activate(language)
        request.LANGUAGE_CODE = language
