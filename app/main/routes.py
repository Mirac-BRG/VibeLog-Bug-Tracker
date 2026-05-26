import os
import time
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import current_user, login_required
from app import db
from app.main import main
from app.models import Project, BugTicket
from app.main.forms import ProjectForm, BugTicketForm, UpdateProfileForm

@main.route('/')
@login_required
def index():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('main/index.html', title='Projelerim', projects=projects)

@main.route('/project/new', methods=['GET', 'POST'])
@login_required
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            name=form.name.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(project)
        db.session.commit()
        flash('Proje başarıyla oluşturuldu!', 'success')
        return redirect(url_for('main.index'))
    return render_template('main/new_project.html', title='Yeni Proje Ekle', form=form)

@main.route('/project/<int:id>')
@login_required
def project_detail(id):
    project = db.session.get(Project, id)
    if project is None:
        abort(404)
    if project.user_id != current_user.id:
        abort(403)
        
    page = request.args.get('page', 1, type=int)
    # Using dynamic querying to paginate bug tickets
    # In models.py we have bug_tickets as a list, but we can query BugTicket model directly
    pagination = BugTicket.query.filter_by(project_id=project.id).order_by(BugTicket.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('main/project_detail.html', title=project.name, project=project, pagination=pagination)

@main.route('/project/<int:project_id>/bug/new', methods=['GET', 'POST'])
@login_required
def new_bug(project_id):
    project = db.session.get(Project, project_id)
    if project is None:
        abort(404)
    if project.user_id != current_user.id:
        abort(403)
        
    form = BugTicketForm()
    if form.validate_on_submit():
        bug = BugTicket(
            title=form.title.data,
            description=form.description.data,
            project_id=project.id,
            status='Open' # varsayılan statü
        )
        db.session.add(bug)
        db.session.commit()
        flash('Bug başarıyla eklendi!', 'success')
        return redirect(url_for('main.project_detail', id=project.id))
    return render_template('main/new_bug.html', title='Yeni Bug Ekle', form=form, project=project)

@main.route('/bug/<int:id>/resolve', methods=['POST'])
@login_required
def resolve_bug(id):
    bug = db.session.get(BugTicket, id)
    if bug is None:
        abort(404)
    if bug.project.user_id != current_user.id:
        abort(403)
        
    bug.status = 'Closed'
    db.session.commit()
    flash(f'Bug "{bug.title}" çözüldü olarak işaretlendi.', 'success')
    return redirect(url_for('main.project_detail', id=bug.project_id))

@main.route('/bug/<int:bug_id>')
@login_required
def bug_detail(bug_id):
    bug = db.session.get(BugTicket, bug_id)
    if bug is None:
        abort(404)
    if bug.project.user_id != current_user.id:
        abort(403)
        
    return render_template('main/bug_detail.html', title=bug.title, bug=bug)

@main.route('/search')
@login_required
def search():
    q = request.args.get('q', '').strip()
    if not q:
        flash('Lütfen aramak için bir kelime girin.', 'warning')
        return redirect(request.referrer or url_for('main.index'))
        
    page = request.args.get('page', 1, type=int)
    
    pagination = BugTicket.query.join(Project).filter(
        Project.user_id == current_user.id,
        (BugTicket.title.ilike(f'%{q}%') | BugTicket.description.ilike(f'%{q}%'))
    ).order_by(BugTicket.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('main/search_results.html', title='Arama Sonuçları', pagination=pagination, q=q)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.avatar.data:
            avatar_file = form.avatar.data
            filename = secure_filename(avatar_file.filename)
            ext = os.path.splitext(filename)[1]
            new_filename = f"user_{current_user.id}_{int(time.time())}{ext}"
            
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'avatars')
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, new_filename)
            avatar_file.save(file_path)
            
            current_user.avatar_image = new_filename
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.dark_mode = form.dark_mode.data
        
        db.session.commit()
        flash('Hesabınız başarıyla güncellendi!', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.dark_mode.data = current_user.dark_mode
        
    return render_template('main/profile.html', title='Profilim', form=form)

@main.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title='Sayfa Bulunamadı'), 404

@main.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', title='Sunucu Hatası'), 500
