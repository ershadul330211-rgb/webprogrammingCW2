import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Character, Quote

@csrf_exempt
@require_http_methods(["GET", "POST"])
def character_list_create(request):
    """
    GET: Returns a list of all characters.
    POST: Creates a new character.
    """
    if request.method == 'GET':
        characters = Character.objects.all().order_by('name')
        data = [char.to_dict() for char in characters]
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            character = Character.objects.create(
                name=data['name'],
                description=data['description'],
                age=data.get('age', None),
                birthday=data.get('birthday', None),
                is_samurai=data.get('is_samurai', False)
            )
            return JsonResponse(character.to_dict(), status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PUT", "DELETE"])
def character_detail_update_delete(request, pk):
    """
    PUT: Updates a single character.
    DELETE: Deletes a single character.
    """
    try:
        character = Character.objects.get(pk=pk)
    except Character.DoesNotExist:
        return JsonResponse({'error': 'Character not found'}, status=404)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            character.name = data.get('name', character.name)
            character.description = data.get('description', character.description)
            character.age = data.get('age', character.age)
            character.birthday = data.get('birthday', character.birthday)
            character.is_samurai = data.get('is_samurai', character.is_samurai)
            character.save()
            character.refresh_from_db()
            return JsonResponse(character.to_dict())
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'DELETE':
        character.delete()
        return HttpResponse(status=204) # 204 No Content

@csrf_exempt
@require_http_methods(["POST"]) 
def quote_create(request):
    """
    POST: Creates a new quote for a specific character.
    """
    try:
        data = json.loads(request.body)
        character = Character.objects.get(pk=data['character_id'])
        Quote.objects.create(
            character=character,
            text=data['text'],
        )
        character.refresh_from_db() # Get the updated list of quotes
        return JsonResponse(character.to_dict(), status=201)
    except Character.DoesNotExist:
        return JsonResponse({'error': 'Character not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PUT", "DELETE"])
def quote_detail_update_delete(request, pk):
    """
    PUT: Updates a single quote.
    DELETE: Deletes a single quote.
    """
    try:
        quote = Quote.objects.get(pk=pk)
    except Quote.DoesNotExist:
        return JsonResponse({'error': 'Quote not found'}, status=44)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            quote.text = data.get('text', quote.text)
            quote.save()
            
            quote.character.refresh_from_db() # Get updated parent
            return JsonResponse(quote.character.to_dict())
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'DELETE':
        character = quote.character # Get parent character
        quote.delete()
        character.refresh_from_db() # Get updated parent
        return JsonResponse(character.to_dict())