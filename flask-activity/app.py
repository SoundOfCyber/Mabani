from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config')

class book(db.Model):
  __tablename__ = 'books'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)
  completed = db.Column(db.Boolean, nullable=False)

@app.route('/')
def index():
    return render_template('my-books.html', books=[ 
        {
            'title': 'A Mind for Numbers',
            'author': 'Barbara Oakley',
            'type': 'Science',
            'read': True
        },
        {
            'title': 'Designing Your Life',
            'author': 'Bill Burnett, Dave Evans',
            'type': 'Life',
            'read': True
        },
        {
            'title': 'A Breif History of Time',
            'author': 'Stephen Hawking',
            'type': 'Science',
            'read': False
        }])
# TODO: implment a GET request to fetch all books

@app.route('/add-book')
def addBook():
    return render_template('add-book.html')
    
# TODO: implment a POST request of adding a book
 @app.route('/main', methods=['POST'])
def create_book():
  error = False
  body = {}
  try:
    description = request.get_json()['description']
    book = books(description=description, completed=False)
    db.session.add(book)
    db.session.commit()
    body['id'] = book.id
    body['completed'] = book.completed
    body['description'] = book.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)
# TODO: implment a PUT request to mark the book as read
# TODO: implment a Delete request to delete a book
@app.route('/my-books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
  try:
    Todo.query.filter_by(id=book_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({ 'success': True })
# Default port:
if __name__ == '__main__':
    app.run(debug=True)