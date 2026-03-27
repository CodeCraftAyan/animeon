from flask import Flask, render_template, request
import requests

app = Flask(__name__)
url = 'https://api.jikan.moe/v4/'

@app.route('/')
def get_characters_data():
    response = requests.get(url + 'characters')
    if response.status_code != 200:
        return "API Error", 500

    data = response.json()

    context = {
        'characters': data['data'],
    }
    return render_template('index.html', **context)

@app.route('/anime')
def get_anime_video():
    response = requests.get(url + 'anime')
    if response.status_code != 200:
        return "API Error!", 500
    
    data = response.json()
    context = {
        'videos' : data['data'],
    }
    return render_template('anime.html', **context)

@app.route('/manga')
def get_manga_data():
    response = requests.get(url + 'manga')
    if response.status_code != 200:
        return "API error!", 500
    
    data = response.json()
    context = {
        'mangas': data['data'],
    }
    return render_template('manga.html', **context)

@app.route('/people')
def get_people_data():
    response = requests.get(url + 'people')
    if response.status_code != 200:
        return 'API Error!', 500
    
    data = response.json()
    context = {
        'peoples': data['data'],
    }
    return render_template('people.html', **context)

@app.route('/random', methods=['GET', 'POST'])
def get_random_data():
    choose = None
    if request.method == 'POST':
        choose = request.form.get('random_option')
    
    if not choose:
        choose = 'anime'

    sub_url = f"random/{choose}"
    response = requests.get(url + sub_url)
    if response.status_code != 200:
        return "API error!", 500
    
    data = response.json()
    context = {
        'random': data['data'],
    }
    return render_template('random.html', **context)

@app.route('/search')
def get_search_data():
    query = request.args.get('q')
    search_type = request.args.get('type', 'anime')
    page = request.args.get('page', 1, type=int)

    results = []
    pagination = {}

    if query:
        response = requests.get(
            f"{url}{search_type}?q={query}&page={page}"
        )

        if response.status_code == 200:
            data = response.json()
            results = data['data']
            pagination = data['pagination']

    return render_template(
        'search.html',
        results=results,
        query=query,
        search_type=search_type,
        page=page,
        pagination=pagination
    )



if __name__ == "__main__":
    app.run(debug=True)