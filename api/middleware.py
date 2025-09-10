from django.http import JsonResponse 

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  
    
    def __call__(self, request):
        
        if request.META.get('HTTP_X_API_KEY') != 'demo':  
            return JsonResponse({'error': 'Invalid API key'}, status=401)
        
        return self.get_response(request)