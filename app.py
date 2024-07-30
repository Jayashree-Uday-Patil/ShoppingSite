from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'e-shopping'
app.config['SESSION_TYPE']=''
app.config['SECRET_KEY']='super secret key'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account')
def account():

    return render_template('account.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/single')
def single():
    return render_template('single.html')

@app.route('/men')
def men():
    return render_template('men.html')

@app.route('/women')
def women():
    return render_template('women.html')


@app.route('/Placed')
def Placed():
    return render_template('placed.html')

@app.route('/User_Feedback')
def User_Feedback():
    return render_template('Feedback.html')



@app.route('/Buy')
def Buy():
    return redirect(url_for('Pay'))

@app.route('/Pay')
def Pay():
    return render_template('pay.html')



@app.route('/User_signup',methods=['POST','GET'])
def User_signup():
    status = True
    if request.method == "POST":
        details = request.form
        fname = details['txt_fname']
        lname = details['txt_lname']
        contact = details['txt_contact']
        address = details['txt_address']
        email = details['txt_email']
        password = details['txt_password']
        cur = mysql.connection.cursor()
        cur.execute("insert into signup_tbl (fname,lname,contact,address,email,password) values(%s,%s,%s,%s,%s,%s)",
                    (fname, lname,contact, address,email, password))
        mysql.connection.commit()
        cur.close()
        return "Record Inserted"
    return render_template('user_signup.html')



@app.route('/User_login', methods=['POST', 'GET'])
def User_login():
    status = True
    if request.method == "POST":
        details = request.form
        username = details['txt_username']
        password = details['txt_pass']
        cur = mysql.connection.cursor()
        cur.execute("select * from signup_tbl where email=%s and password=%s",(username,password))
        data=cur.fetchone()
        if data:
            session['logged_in']=True
            session['Fname']=data[1]
            session['Lname'] = data[2]
            session['num'] = data[3]
            session['add'] = data[4]


            return redirect('View_women')
        else:
            return render_template('user_login.html')

    return render_template('user_login.html')


@app.route('/Admin_login')
def admin_login():
    mail = "admin@gmail.com"
    password = "1234"
    if mail == "admin@gmail.com" and password == "1234":
        return redirect('/Add_mens_product')
    else:
        return render_template('admin_login.html')




@app.route('/View_men',methods=['POST','GET'])
def View_men():
    cur = mysql.connection.cursor()
    cur.execute("select * from mens_product")
    data = cur.fetchall()


    return render_template('view_men_product.html', value=data)



@app.route('/View_women',methods=['POST','GET'])
def View_women():
    cur = mysql.connection.cursor()
    cur.execute("select * from womens_product")
    data = cur.fetchall()
    return render_template('view_women_product.html', value=data)



@app.route('/View_kids',methods=['POST','GET'])
def View_kids():
    cur = mysql.connection.cursor()
    cur.execute("select * from kids_product")
    data = cur.fetchall()
    return render_template('view_kids_product.html', value=data)

@app.route('/Add_mens_product', methods=['POST', 'GET'])
def Add_mens_product():
    status = True
    if request.method == "POST":
        details = request.form

        pname = details['txt_pname']
        pimage = "static/images/" + details['txt_pimage']
        pprice = details['txt_pprice']
        pdes = details['txt_pdes']
        cur = mysql.connection.cursor()
        cur.execute("insert into mens_product(name,image,price,description) values(%s,%s,%s,%s)",
                    ( pname, pimage, pprice, pdes))
        mysql.connection.commit()
        cur.close()
        return "Record Inserted"

    return render_template('add_men_product.html')


@app.route('/Show_men_products')
def Show_men_products():
    cur = mysql.connection.cursor()
    cur.execute("select * from mens_product ")
    data = cur.fetchall()
    return render_template('show_men_product.html', value=data)


@app.route('/delete_men_product', methods=['POST', 'GET'])
def delete_men_product():
    status = True
    if request.method == "POST":
        details = request.form
        id = details['txt_id']
        cur = mysql.connection.cursor()
        cur.execute("delete from mens_product where id=%s", (id))
        mysql.connection.commit()
        cur.close()
        return redirect('Show_men_products')

    return render_template('show_men_products.html')


@app.route('/update_men_product', methods=['POST', 'GET'])
def update_men_product():
    status = True
    if request.method == "POST":
        details = request.form
        id = details['txt_id']
        pname = details['txt_pname']
        pimage = details['txt_pimage']
        price = details['txt_price']
        desc = details['txt_desc']

        cur = mysql.connection.cursor()
        cur.execute("update mens_product set  name=%s,image=%s,price=%s,description=%s where id=%s",
                    (pname, pimage, price, desc, id))
        mysql.connection.commit()
        cur.close()
        return redirect('Show_men_products')
    return render_template('show_men_product.html')


#Women

@app.route('/Add_womens_product', methods=['POST', 'GET'])
def Add_womens_product():
    status = True
    if request.method == "POST":
        details = request.form

        pname = details['txt_pname']
        pimage = "static/images/" + details['txt_pimage']
        pprice = details['txt_pprice']
        pdes = details['txt_pdes']
        cur = mysql.connection.cursor()
        cur.execute("insert into womens_product(name,image,price,description) values(%s,%s,%s,%s)",
                    ( pname, pimage, pprice, pdes))
        mysql.connection.commit()
        cur.close()
        return "Record Inserted"

    return render_template('add_women_product.html')


@app.route('/Show_women_products')
def Show_women_products():
    cur = mysql.connection.cursor()
    cur.execute("select * from womens_product ")
    data = cur.fetchall()
    return render_template('show_women_product.html', value=data)


@app.route('/delete_women_product', methods=['POST', 'GET'])
def delete_women_product():
    status = True
    if request.method == "POST":
        details = request.form
        id = details['txt_id']
        cur = mysql.connection.cursor()
        cur.execute("delete from womens_product where id=%s", (id))
        mysql.connection.commit()
        cur.close()
        return redirect('Show_women_products')

    return render_template('show_women_product.html')


@app.route('/update_women_product', methods=['POST', 'GET'])
def update_women_product():
    status = True
    if request.method == "POST":
        details = request.form
        id = details['txt_id']
        pname = details['txt_pname']
        pimage = details['txt_pimage']
        price = details['txt_price']
        desc = details['txt_desc']

        cur = mysql.connection.cursor()
        cur.execute("update womens_product set  name=%s,image=%s,price=%s,description=%s where id=%s",
                    (pname, pimage, price, desc, id))
        mysql.connection.commit()
        cur.close()
        return redirect('Show_women_products')
    return render_template('show_women_product.html')


#Kids

@app.route('/Add_kids_product', methods=['POST', 'GET'])
def Add_kids_product():
    status = True
    if request.method == "POST":
        details = request.form

        pname = details['txt_pname']
        pimage = "static/images/" + details['txt_pimage']
        pprice = details['txt_pprice']
        pdes = details['txt_pdes']
        cur = mysql.connection.cursor()
        cur.execute("insert into kids_product(name,image,price,description) values(%s,%s,%s,%s)",
                    ( pname, pimage, pprice, pdes))
        mysql.connection.commit()
        cur.close()
        return "Record Inserted"

    return render_template('add_kids_product.html')

@app.route('/Show_kids_products')
def Show_kids_products():
    cur = mysql.connection.cursor()
    cur.execute("select * from kids_product ")
    data = cur.fetchall()
    return render_template('show_kids_product.html', value=data)


@app.route('/delete_kid_product', methods=['POST', 'GET'])
def delete_kid_product():
    status = True
    if request.method == "POST":
        details = request.form
        id = details['txt_id']
        cur = mysql.connection.cursor()
        cur.execute("delete from kids_product where id=%s", (id))
        mysql.connection.commit()
        cur.close()
        return redirect('Show_kids_products')

    return render_template('show_kid_product.html')


@app.route('/update_kid_product', methods=['POST', 'GET'])
def update_kid_product():
    status = True
    if request.method == "POST":
        details = request.form
        id = details['txt_id']
        pname = details['txt_pname']
        pimage = details['txt_pimage']
        price = details['txt_price']
        desc = details['txt_desc']

        cur = mysql.connection.cursor()
        cur.execute("update kids_product set  name=%s,image=%s,price=%s,description=%s where id=%s",
                    (pname, pimage, price, desc, id))
        mysql.connection.commit()
        cur.close()
        return redirect('Show_kids_products')
    return render_template('show_kid_product.html')

# dislay actual price of particular product
@app.route('/kids_products',methods=['POST','GET'])
def kids_products():
    status=True
    if request.method=="POST":
        details=request.form
    return render_template('pay.html', **details)

@app.route('/Women_products',methods=['POST','GET'])
def Women_products():
    status=True
    if request.method=="POST":
        details=request.form
    return render_template('pay.html', **details)

@app.route('/Men_products',methods=['POST','GET'])
def Men_products():
    status=True
    if request.method=="POST":
        details=request.form
    return render_template('pay.html', **details)


@app.route('/kids_names',methods=['POST','GET'])
def kids_names():
    status=True
    if request.method=="POST":
        details=request.form
    return render_template('pay.html', **details)


if __name__ == "__main__":
    app.debug = True
    app.run()
