from flask import Flask, render_template, request, redirect, url_for

from models import db, Tb1

from sqlalchemy import update, delete


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

#@app.before_first_request
@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def list_records():
    tb1fieldNamesNoIds = Tb1.get_field_names_noIds()
    print ('tb1fieldNamesNoIds')
    print (tb1fieldNamesNoIds)

    tb1s = Tb1.query.all()
    return render_template('list_records.html', tb1s=tb1s, tb1fieldNamesNoIds=tb1fieldNamesNoIds )

# Create a new record
@app.route('/create', methods=['GET', 'POST'])
def create_record():
    tb1fieldNamesNoIds = Tb1.get_field_names_noIds()

    if request.method == 'POST':
        data = {tb1fieldNamesNoId: request.form[tb1fieldNamesNoId] for tb1fieldNamesNoId in tb1fieldNamesNoIds}

        new_tb1 = Tb1(**data)
        db.session.add(new_tb1)

        db.session.commit()
        return redirect(url_for('list_records'))
    return render_template('create.html', tb1fieldNamesNoIds=tb1fieldNamesNoIds)

# Update a student
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_record(id):

    tb1fieldNamesNoIds = Tb1.get_field_names_noIds()
    record = db.session.query(Tb1).filter(Tb1.id == id).first()
    print ('record')
    print (record)
    if request.method == 'POST':

        for tb1fieldNamesNoId in tb1fieldNamesNoIds:
            
            Tb1.tb1fieldNamesNoId = request.form[tb1fieldNamesNoId]
            print ('Tb1.tb1fieldNamesNoId')
            print (Tb1.tb1fieldNamesNoId)
            setattr(record, tb1fieldNamesNoId, Tb1.tb1fieldNamesNoId)
        
        db.session.commit()
        return redirect(url_for('list_records'))

    return render_template('update.html', record=record, tb1fieldNamesNoIds=tb1fieldNamesNoIds)


# Delete a record
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_record(id):
    # Get the record or return 404 if not found
    record = Tb1.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            db.session.delete(record)  # Correct method to delete
            db.session.commit()
            ##flash('Record deleted successfully', 'success')
            return redirect(url_for('list_records'))  # Ensure this is your correct endpoint
        except Exception as e:
            db.session.rollback()
            ##flash(f'Error deleting record: {str(e)}', 'error')
            return redirect(url_for('list_records'))

    return render_template('delete.html', record=record)



'''

# Delete a record
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_record(id):
    tb1fieldNamesNoIds = Tb1.get_field_names_noIds()
    record = db.session.query(Tb1).filter(Tb1.id == id).first()
    if request.method == 'POST':
        db.session.delete_record(id)
        db.session.commit()
        return redirect(url_for('list_records'))

    return render_template('delete.html', record=record)

'''

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
