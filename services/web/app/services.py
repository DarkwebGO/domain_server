from . import models

def get_all_entries():
    return models.Darkweb.query.all()

def get_active_tasks(page, items_per_page):
    return models.UrlWeb.query.filter_by(status='true').paginate(page=page, per_page=items_per_page, error_out=False)

def get_inactive_tasks(page, items_per_page):
    return models.UrlWeb.query.filter_by(status='false').paginate(page=page, per_page=items_per_page, error_out=False)

def get_random_false_domain():
    return models.UrlWeb.query.filter_by(status='false').order_by(models.db.func.random()).first()

def update_false_domain_to_true(url_web):
    if url_web:
        url_web.status = 'true'
        models.db.session.commit()
        return url_web
    return None