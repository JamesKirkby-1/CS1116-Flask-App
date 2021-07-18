#Imports
from flask import Flask, render_template, session, request, redirect, url_for, g, flash
from database import get_db, close_db
from forms import RegistrationForm, LoginForm, CheckoutForm, PasswordForm
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

#Instatiate Flask object named app
app = Flask(__name__)

#Configure security key
app.config["SECRET_KEY"] = "this-is-my-secret-key"

#Configure sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Close database
@app.teardown_appcontext
def close_db_at_end_of_requests(e=None):
    close_db(e)

#Configure user session
@app.before_request
def load_logged_in_user():
    g.user = session.get("username",None)

#Configure login requirement
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return view(**kwargs)
    return wrapped_view

#Route for home page
@app.route("/")
def index():
    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()
    return render_template("index.html", title="Home", products=products)

#Route for sign up 
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #Variables
        username = form.username.data
        email = form.email.data
        password = form.password.data
        #Check if username already in database
        db = get_db()
        check_username = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        check_email = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        #If new user, upload info into the users database
        if check_username is None:
            if check_email is None:
                db = get_db()
                db.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (username,email,generate_password_hash(password)))
                db.commit()
                flash(f'Account created for {form.username.data}!', 'success')
                return redirect(url_for('login'))
            #If email already exists, display error message
            else:
                flash('That email is already taken. Please choose another one.', 'danger')
        #If username already exists, display error message        
        else:
            flash('That username is already taken. Please choose another one.', 'danger')
    return render_template("register.html", title="Sign Up", form=form)

#Route for login (safe)
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?",(username,)).fetchone()
        #If username does not exist in user database
        if user is None:
            flash('Login Unsuccessful! Please check username and password.', 'danger')
        #If password does not match password in user database    
        elif not check_password_hash(user["password"],password):
            flash('Login Unsuccessful! Please check username and password.', 'danger')
        else:
            session.clear()
            session["username"] = username
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("index")
                flash('You have been logged in!', 'success')
            return redirect(next_page)
    return render_template("login.html", title="Login", form=form)

#Route for logout (safe)
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

#Route for shopping cart 
@app.route("/cart")
@login_required
def cart():
    #Check if cart is in session
    if "cart" not in session:
        session["cart"] = {}
    #Initialise variables
    names = {}
    prices = {}
    subtotals = {}
    total = 0
    db = get_db()
    #Loop through each item in cart
    for product_id in session["cart"]:
        name = db.execute("SELECT * FROM products WHERE product_id=?",(product_id,)).fetchone()["name"]
        names[product_id] = name
        price = db.execute("SELECT * FROM products WHERE product_id=?",(product_id,)).fetchone()["price"]
        prices[product_id] = price
        #Find subtotals
        subtotal = session["cart"][product_id] * price
        subtotals[product_id] = subtotal
        #Find total price
        total = sum(subtotals.values())
    db.close()
    return render_template("cart.html", title="Your Cart", cart=session["cart"], names=names, prices=prices, subtotals=subtotals, total=total)

#Route for add to cart 
@app.route("/add_to_cart/<int:product_id>")
@login_required
def add_to_cart(product_id):
    #Check if cart is in session
    if "cart" not in session:
        session["cart"] = {}
    if product_id not in session["cart"]:
        session["cart"][product_id] = 0
    #Increase quantity by 1
    session["cart"][product_id] = session["cart"][product_id] + 1
    print(session["cart"])
    return redirect( url_for("cart"))

#Route for remove from cart (test)
@app.route("/remove_from_cart/<int:product_id>")
@login_required
def remove_from_cart(product_id):
    #Check if cart is in session
    if "cart" not in session:
        session["cart"] = {}
    if product_id not in session["cart"]:
        session["cart"][product_id] = 0
    #Decrease quantity by 1
    session["cart"][product_id] = session["cart"][product_id] - 1
    #Removes item from cart when quanity reaches 0
    if session["cart"][product_id] == 0:
        del session["cart"][product_id]
    print(session["cart"])
    return redirect( url_for("cart"))

#Route for checkout page
@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        #Variables for billing
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        address = form.address.data
        address2 = form.address2.data
        country = form.country.data
        city = form.city.data
        postcode = form.postcode.data
        #Check if details already in database (use username as a key)
        db = get_db()
        username = g.user
        user = db.execute("SELECT * FROM details WHERE username = ?", (username,)).fetchone()
        #If username does not exist, upload info to database
        if user is None:
            db = get_db()
            db.execute("INSERT INTO details (firstname, lastname, username, address, address2, country, city, postcode) VALUES (?,?,?,?,?,?,?,?)", (firstname, lastname, username, address, address2, country, city, postcode))
            db.commit()
            flash(f'Order placed! Thank you for shopping with us!', 'success')
            del session["cart"]
            return redirect(url_for('index'))
        #If username does exist, redirect to payment without uploading info to database
        else:
            flash(f'Order placed! Thank you for shopping with us!', 'success')
            del session["cart"]
            return redirect(url_for('index'))     
    return render_template("checkout.html", title="Checkout", form=form)

#Route for password reset
@app.route("/passwordreset", methods=["GET","POST"])
@login_required
def passwordReset():
    #Form for changing password
    form = PasswordForm()
    if form.validate_on_submit():
        currentPassword = form.currentPassword.data
        newPassword = form.newPassword.data
        checkNewPassword = form.checkNewPassword.data
        #Retrieve users current password from database
        db = get_db()
        username = g.user
        user = db.execute("SELECT * FROM users WHERE username = ?",(username,)).fetchone()
        #Display error if user does not exist
        if currentPassword is None:
            flash('Unknown password', 'danger')
        #Display error if passwords do not match
        elif check_password_hash(user["password"], currentPassword):
            if not newPassword == checkNewPassword:
                flash("Passwords do not match.", "danger")
        #Update old password to new password
            else:
                db.execute("UPDATE users SET password = ? WHERE username = ?",((generate_password_hash(newPassword)), username))
                db.commit()
                flash("Password updated!", "success")    
        #Display error if old password does not exist
        elif not check_password_hash(user["password"], currentPassword):
            flash("Current Password is incorrect.", "danger")
    return render_template("passwordReset.html", title="Password Reset", form=form)

#Route for filter name (A-Z)
@app.route("/filter_name_asc")
def filter_name_ASC():
    db = get_db()
    products = db.execute("SELECT * FROM products ORDER BY name ASC").fetchall()
    return render_template("index.html", title="Home", products=products)

#Route for filter name (A-Z)
@app.route("/filter_name_desc")
def filter_name_DESC():
    db = get_db()
    products = db.execute("SELECT * FROM products ORDER BY name DESC").fetchall()
    return render_template("index.html", title="Home", products=products)

#Route for filter price (Low-High)
@app.route("/filter_price_asc")
def filter_price_ASC():
    db = get_db()
    products = db.execute("SELECT * FROM products ORDER BY price ASC").fetchall()
    return render_template("index.html", title="Home", products=products)

#Route for filter price (High-Low)
@app.route("/filter_price_desc")
def filter_price_DESC():
    db = get_db()
    products = db.execute("SELECT * FROM products ORDER BY price DESC").fetchall()
    return render_template("index.html", title="Home", products=products)

#Error handling for 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

#Error handling for 403
@app.errorhandler(403)
def page_not_found(e):
    return render_template('errors/403.html'), 403

#Error handling for 500
@app.errorhandler(500)
def page_not_found(e):
    return render_template('errors/500.html'), 500

            
