import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

ARTICLE_DIRECTORY = 'articles_data'
ARTICLE_FILE = os.path.join(ARTICLE_DIRECTORY, 'articles.json')

if not os.path.exists(ARTICLE_DIRECTORY):
    os.makedirs(ARTICLE_DIRECTORY)

def load_articles():
    if os.path.exists(ARTICLE_FILE):
        with open(ARTICLE_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_articles(articles):
    with open(ARTICLE_FILE, 'w', encoding='utf-8') as file:
        json.dump(articles, file, ensure_ascii=False, indent=4)

def save_article_to_file(article):
    articles = load_articles()
    article_id = len(articles) + 1
    article['id'] = article_id
    article['marked_vocab'] = []
    articles.append(article)
    save_articles(articles)

@app.route('/')
def home():
    articles = load_articles()
    return render_template('index.html', articles=articles)

@app.route('/article/<int:id>')
def article_page(id):
    articles = load_articles()
    article = next((art for art in articles if art['id'] == id), None)
    if article is None:
        return "Bài viết không tồn tại", 404
    return render_template('article_page.html', article=article)

@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.form.get('image', "https://via.placeholder.com/300")
        pinyin = request.form.get('pinyin', '')
        meaning = request.form.get('meaning', '')

        article = {
            "title": title,
            "content": content,
            "pinyin": pinyin,
            "image": image,
            "meaning": meaning,
            "marked_vocab": []
        }
        save_article_to_file(article)
        return redirect(url_for('home'))
    return render_template('add_article.html')

@app.route('/mark_vocab/<int:id>', methods=['POST'])
def mark_vocab(id):  # Change article_id to id
    articles = load_articles()
    article = next((art for art in articles if art['id'] == id), None)
    if article is None:
        return "Bài viết không tồn tại", 404
    word = request.form['word']
    if word not in article['marked_vocab']:
        article['marked_vocab'].append(word)
    save_articles(articles)
    return redirect(url_for('article_page', id=id))

@app.route('/remove_word/<int:id>/<word>', methods=['POST'])
def remove_word(id, word):  # Change article_id to id
    articles = load_articles()
    article = next((art for art in articles if art['id'] == id), None)
    if article is None:
        return "Bài viết không tồn tại", 404
    if word in article['marked_vocab']:
        article['marked_vocab'].remove(word)
    save_articles(articles)
    return redirect(url_for('article_page', id=id))

if __name__ == '__main__':
    app.run(debug=True)
