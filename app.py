from flask import *
from flask_sqlalchemy import SQLAlchemy
from models import *
from fileMethods import *

# Initializing the app
app = Flask(__name__)

# Writing configs for storing DB URI
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///kanban.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating the db
db = SQLAlchemy(app)
db.create_all()


# Routes
@app.route("/add/<int:id>", methods = ["GET", "POST"])
def add(id):
    if request.method == "POST":
        listItems = ListItems(title = request.form['title'],content =  request.form['content'],  deadline = datetime.strptime(request.form['deadline'],"%Y-%m-%dT%H:%M") ,reference=id, username = readFile() )
        db.session.add(listItems)
        db.session.commit()
        return redirect('/index')
    return render_template('add.html')

@app.route("/delete/<int:sno>")
def deleteList(sno):
    kanBanList = KanBanList.query.filter_by(sno = sno).first()
    listItems = ListItems.query.filter_by(reference = sno).all()
    for element in listItems:
        db.session.delete(element)
        db.session.commit()
    db.session.delete(kanBanList)
    db.session.commit()
    return redirect('/index')

@app.route("/updateList/<int:sno>", methods = ["GET", "POST"])
def updateList(sno):
    if request.method == "POST":
        title = request.form['title']
        kanBanList = KanBanList.query.filter_by(sno = sno).first()
        kanBanList.listName = title
        db.session.add(kanBanList)
        db.session.commit()
        return redirect('/index')
    allLists = KanBanList.query.all()
    temp = ''
    for element in allLists:
        if (element.sno==sno):
            temp = element
    
    return render_template('updateList.html', temp = temp)

@app.route("/", methods = ["GET", "POST"])
def sign_in():
    status = True
    if request.method == "POST":
        users = Users.query.filter_by(username = request.form['username'], password = request.form['password']).first()

        if (users):
            writeFile(request.form['username'])
            return redirect('/index')
        else:
            status = False
    return render_template('sign_in.html', status = status)

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        users = Users(username = request.form['username'], password = request.form['password'])
        try:
            db.session.add(users)
            db.session.commit()
        except:
            return render_template("register.html")
        writeFile(request.form['username'])
        return redirect('/index')
    return render_template('register.html')

@app.route("/index", methods = ["GET", "POST"])
def index():
    username = readFile()
    if request.method=="POST":
         kanBanList = KanBanList(listName = request.form['name'], username = username, sno = getCount()) 
         try:
            db.session.add(kanBanList)
            db.session.commit()
         except:
            return url_for("index")
    allLists = KanBanList.query.all()
    listItems = ListItems.query.all()
    return render_template('index.html', allLists = allLists, listItems = listItems, username = username)

@app.route("/updateItems/<int:sno>", methods = ["GET", "POST"])
def updateItems(sno):
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        deadline = datetime.strptime(request.form['deadline'],"%Y-%m-%dT%H:%M")
        listItems = ListItems.query.filter_by(sno = sno).first()
        listItems.completedFlag = request.form['status']
        if (listItems.completedFlag == "on"):
            listItems.timeCompleted = str(datetime.now())
        if (title!=''):
            listItems.title = title
        if (content!=''):
            listItems.content = content
        if (deadline!=''):
            listItems.deadline = deadline
        db.session.add(listItems)
        db.session.commit()
        return redirect('/index')
    my_user = readFile()
    listItems = ListItems.query.filter_by(sno=sno).first()
    allLists = KanBanList.query.all()
    dropList = KanBanList.query.filter_by(username = my_user)
    print(dropList)
    return render_template("updateItems.html", listItems = listItems, allLists = allLists, dropList=dropList)

@app.route("/deleteItem/<int:sno>", methods = ["GET", "POST"])
def deleteItem(sno):
    listItems = ListItems.query.filter_by(sno = sno).first()
    db.session.delete(listItems)
    db.session.commit()
    return redirect('/index')

#To update the list in which the list-item is present.
@app.route("/update-route/<int:lsno>/<int:ksno>", methods = ["GET", "POST"])
def updateRoute(lsno, ksno):
    listItems = ListItems.query.filter_by(sno = lsno).first()
    listItems.reference = ksno
    db.session.add(listItems)
    db.session.commit()
    return redirect('/updateItems/'+str(lsno))

@app.route('/stats')
def displayStats():
    datee = []
    years = []
    data = []
    pendingData = []
    
    #Calculating completed tasks.
    
    listItems = ListItems.query.filter_by(username = readFile())
    for item in listItems:
        if (item.timeCompleted is not None):
            year = item.timeCompleted.split(" ")[0]
            if (item not in years):
                years.append(year)
    for item in listItems:
        if (item.timeCompleted is not None):
            year = item.timeCompleted.split(" ")[0]
            if ([item.timeCompleted.split(" "), years.count(year)] not in datee):
                datee.append([year,years.count(year)])
    for item in datee:
        if item not in data:
            data.append(item)
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    
    #Calculating pending tasks
    
    for item in listItems:
        dateData = item.deadline
        todaysDate = date.today()
        if (dateData < todaysDate):
            if (item.completedFlag=='off'):
                pendingData.append(item)
    return render_template('stats.html', labels = labels, values = values, pendingData = pendingData)

@app.route("/about")
def about():
    return render_template('about.html')

if __name__=="__main__":
    app.run(host="localhost", debug=True)