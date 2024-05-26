from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV= 'prod'

if ENV == "dev":
    app.debug=True 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/practice' #postgresql://username.password@localhost:5432/dbname
  
else:
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://admin:2qaxRvmPJGnE4x3bN7y4yIMeLmTQtBuh@dpg-cp9ftn5ds78s73ch8lng-a/prod_postgres_3w69'
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())
    
    def __init__(self,customer, dealer, rating, comments):
        self.customer = customer 
        self.dealer = dealer 
        self.rating = rating 
        self.comments = comments
        
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=['POST'])
def submit():
    if(request.method=="POST"):
        customer= request.form["customer"]
        Dealer = request.form["Dealer"]
        rating = request.form["rating"]
        comments = request.form["comments"]
        #print(customer, Dealer, rating, comments)
        if(customer=="" and Dealer== ""):
            return render_template("index.html", message="Please enter required fields")
        
        if(db.session.query(Feedback).filter(Feedback.customer == customer).count()==0):
            data = Feedback(customer, Dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, Dealer, rating, comments)
            return render_template("success.html")
        else:
            return render_template("index.html", message="You have already submitted feedback")
        



# if __name__ == "__main__":
#     app.run()