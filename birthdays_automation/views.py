import os
from pathlib import Path
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import uuid
from more_itertools import chunked
from django.shortcuts import redirect

def redirect_to_upload(request):
    return redirect('/birthdays_automation/upload/')

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

        aniversariantes = df.to_dict(orient='records')
        current_month = meses[str(aniversariantes[0]['MES'])]
        year = datetime.now().year 

        font_path = os.path.join(settings.STATICFILES_DIRS[0], 'arial_black.ttf')
        template_path = os.path.join(settings.STATICFILES_DIRS[0], 'template.png')

        if not os.path.exists(font_path):
            return JsonResponse({'error': 'Fonte não encontrada'}, status=500)

        font = ImageFont.truetype(font_path, size=38)
        fontLineTwo = ImageFont.truetype(font_path, size=25)
        fontTitleMonth = ImageFont.truetype(font_path, size=58)

        new_list = list(chunked(aniversariantes, 7))
    
        order = 1
        image_urls = []
        for value in new_list:
            template = Image.open(template_path)
            draw = ImageDraw.Draw(template)  
            
            title = current_month.upper() + ' ' + str(year)
            title_bbox = draw.textbbox((0, 0), title, font=fontTitleMonth)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (template.width - title_width) / 2 

            draw.text((title_x, 470), title, fill='white', font=fontTitleMonth) 

            y = 700
            for aniversariante in value:
                name = aniversariante['NOME']
                day = aniversariante['DIA']
                month = aniversariante['MES']

                if month <= 9:
                    month = '0' + str(month)

                line_one = f"{day}/{month} {name.upper()}"
                line_one_bbox = draw.textbbox((0, 0), line_one, font=font)
                line_one_width = line_one_bbox[2] - line_one_bbox[0]
                line_one_x = (template.width - line_one_width) / 2 

                draw.text((line_one_x, y), line_one, fill='#1f3864', font=font)
                y += 55

                description = aniversariante['DESCRICAO']
                description_bbox = draw.textbbox((0, 0), description, font=fontLineTwo)
                description_width = description_bbox[2] - description_bbox[0]
                description_x = (template.width - description_width) / 2 

                draw.text((description_x, y), description, fill='#1f3864', font=fontLineTwo)
                y += 100

            generated_dir = Path(settings.MEDIA_ROOT) / 'imagens_geradas'
            generated_dir.mkdir(parents=True, exist_ok=True)

            generated_image_path = generated_dir / f'aniversariantes-{current_month.lower()}-{order}-{uuid.uuid4()}.png'
            template.save(str(generated_image_path))

            image_url = os.path.join(settings.MEDIA_URL, 'imagens_geradas', os.path.basename(generated_image_path))
            image_urls.append(image_url)

            order += 1        

        return JsonResponse({'aniversariantes': aniversariantes, 'image_urls': image_urls})

    return render(request, 'upload_file.html')
