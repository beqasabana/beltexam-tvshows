from flask_app import app
from flask import render_template, redirect, request, session, flash
from datetime import datetime
from flask_app.models.show import Show
from flask_app.models.user import User



@app.route('/add/show', methods=['POST'])
def save_report():
    data = {
        'user_id': session['user'],
        'title': request.form['title'],
        'network': request.form['network'],
        'release_date': request.form['release_date'],
        'description': request.form['description']
    }
    if not Show.validate_show(request.form):
        return redirect('/add')
    Show.save(data)
    return redirect('/dashboard')

@app.route('/one/show/<int:show_id>')
def display_one(show_id):
    data = {
        'id': show_id
    }
    show = Show.get_by_id(data)
    return render_template('one_show.html', active_show=show)

@app.route('/delete/<int:show_id>')
def delete_show(show_id):
    data = {
        'id': show_id
    }
    Show.delete(data)
    return redirect('/dashboard')

@app.route('/edit/<int:show_id>')
def display_edit_page(show_id):
    data = {
        'id': show_id
    }
    show = Show.get_by_id(data)
    return render_template('edit.html', active_show=show)

@app.route('/update/show/<int:show_id>', methods=['POST'])
def edit_report(show_id):
    data = {
        'id': show_id,
        'title': request.form['title'],
        'network': request.form['network'],
        'release_date': request.form['release_date'],
        'description': request.form['description']
    }
    if not Show.validate_show(request.form):
        return redirect(f"/edit/{show_id}")
    Show.edit(data)
    return redirect('/dashboard')

@app.route('/like/<int:show_id>')
def like(show_id):
    data = {
        'user_id': session['user'],
        'show_id': show_id
    }
    Show.like(data)
    return redirect('/dashboard')

@app.route('/unlike/<int:show_id>')
def unlike(show_id):
    data = {
        'user_id': session['user'],
        'show_id': show_id
    }
    Show.unlike(data)
    return redirect('/dashboard')