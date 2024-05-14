import os
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import uuid

def upload_file_view(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        df = pd.read_excel(uploaded_file)

        meses = {
            "1": "Janeiro",
            "2": "Fevereiro",
            "3": "Março",
            "4": "Abril",
            "5": "Maio",
            "6": "Junho",
            "7": "Julho",
            "8": "Agosto",
            "9": "Setembro",
            "10": "Outubro",
            "11": "Novembro",
            "12": "Dezembro"
        }

        # Converter o DataFrame em uma lista de dicionários
        aniversariantes = df.to_dict(orient='records')
        print(aniversariantes)

        template_path = os.path.join(settings.STATIC_ROOT, 'template.png')
        template = Image.open(template_path)
        draw = ImageDraw.Draw(template)
        font = ImageFont.truetype('arial.ttf', size=30)
        fontTitleMonth = ImageFont.truetype('arialbd.ttf', size=60)
        month = meses[str(aniversariantes[0]['MES'])]
        year = datetime.now().year    

        draw.text((600, 480), month.upper() + ' ' + str(year), fill='white', font=fontTitleMonth) 

        y = 650
        for aniversariante in aniversariantes:
            nome = aniversariante['NOME']
            draw.text((400, y), nome, fill='black', font=font)
            y += 30

        # Salvando a imagem gerada
        generated_image_path = os.path.join(settings.MEDIA_ROOT, f'{uuid.uuid4()}.png')
        template.save(generated_image_path)

        # Retorne os nomes dos aniversariantes e a URL para a arte gerada
        return JsonResponse({'aniversariantes': aniversariantes, 'arte_url': generated_image_path})

    return render(request, 'upload_file.html')
