from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd

def upload_file_view(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        df = pd.read_excel(uploaded_file)

        # Converter o DataFrame em uma lista de dicionários
        aniversariantes = df.to_dict(orient='records')
        print(aniversariantes)

        # Suponha que você tenha uma lista de aniversariantes
        # aniversariantes = ['João', 'Maria', 'Pedro']

        # Gere a arte com os nomes dos aniversariantes
        # Aqui você pode usar bibliotecas para gerar imagens, como o Pillow

        # Retorne os nomes dos aniversariantes e a URL para a arte gerada
        return JsonResponse({'aniversariantes': aniversariantes, 'arte_url': settings.STATIC_URL + 'template.png'})

    return render(request, 'upload_file.html')
