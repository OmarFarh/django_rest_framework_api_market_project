from django.http import JsonResponse



def handler404(request , exception):

    message = ('Not Found Page')
    response = JsonResponse({'erro':message})
    response.status_code = 404
    return response