from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name


@app.route('/')
def get_all_posts():  # put application's code here
    posts = Post.query.all()
    return render_template("index.html", posts = posts)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    fetched_post = Post.query.get(post_id)
    return render_template("post.html", post = fetched_post)

@app.route('/create-post', methods=['GET', 'POST'])
def create_post():
    if request.method == "GET":
        return render_template("create-post.html")
    else:
        category_name = request.form["category"]
        category = Category(name=category_name)
        post = Post(
            title = request.form["title"],
            subtitle = request.form["subtitle"],
            body = request.form["body"],
            category = category
        )
        db.session.add(post)
        db.session.commit()
        # return f"Post entitled {request.form('title')} added to database!" -> this line isn't working but the rest are
        return redirect(url_for("get_all_posts"))

if __name__ == '__main__':
    app.run()
