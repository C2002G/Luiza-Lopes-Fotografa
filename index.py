from flask import Flask, render_template
import os

app = Flask(__name__)

# Configuração das categorias e fotos
CATEGORIES = {
    'casamentos': 'Casamentos',
    'torcida': 'Torcida',
    'natureza': 'Natureza'
}

def get_photos_from_category(category):
    # Pega todas as fotos da pasta da categoria
    photos_path = os.path.join('static', 'images', category)
    photos = []
    if os.path.exists(photos_path):
        for photo in os.listdir(photos_path):
            if photo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                photos.append({
                    'url': f'/static/images/{category}/{photo}',
                    'title': photo.split('.')[0].replace('_', ' ').title()
                })
    return photos

@app.route('/')
def home():
    # Cria lista de categorias com uma foto de preview
    categories_data = []
    for category_id, category_name in CATEGORIES.items():
        photos = get_photos_from_category(category_id)
        preview_image = photos[0]['url'] if photos else None
        categories_data.append({
            'id': category_id,
            'name': category_name,
            'preview': preview_image
        })
    return render_template('home.html', categories=categories_data)

@app.route('/category/<category_id>')
def category(category_id):
    if category_id not in CATEGORIES:
        return "Categoria não encontrada", 404
    
    photos = get_photos_from_category(category_id)
    return render_template('category.html', 
                         category_name=CATEGORIES[category_id],
                         photos=photos)

if __name__ == '__main__':
    app.run(debug=True)