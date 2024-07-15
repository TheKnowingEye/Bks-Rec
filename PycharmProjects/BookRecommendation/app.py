from flask import Flask, render_template, request
import pickle
import pandas
import numpy as np
with open("popular_df.pkl", 'rb') as file:
    popular = pickle.load(file)

with open("pt.pkl", 'rb') as file:
    pt = pickle.load(file)

with open("books.pkl", 'rb') as file:
    books = pickle.load(file)

with open("sim_score.pkl", 'rb') as file:
    sim_score = pickle.load(file)
app = Flask(__name__)

popular['avg_ratings'] = popular['avg_ratings'].round(1)
@app.route('/')


def index():
    popular['Image-URL-M'] = popular['Image-URL-M'].str.replace('http://', 'https://')
    return render_template('index.html',
                           book_name = list(popular['Book-Title'].values),
                           book_author = list(popular['Book-Author'].values),
                           book_image = list(popular['Image-URL-M'].values),
                           book_rating = list(popular['avg_ratings'].values),
                           book_votes=list(popular['num_ratings'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('Recommend.html',
                           )

@app.route('/recommend_books', methods=['post'])
def recommend_books():
    books['Image-URL-M'] = books['Image-URL-M'].str.replace('http://', 'https://')
    user_input = request.form.get('user_input')
    index_book = np.where(pt.index == user_input)[0][0]
    distance = sim_score[index_book]
    similar_items = sorted(list(enumerate(distance)), key=lambda x: x[1], reverse=True)[1:5]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)
    return render_template('Recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)