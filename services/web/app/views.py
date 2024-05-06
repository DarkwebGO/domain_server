from flask import Blueprint, render_template, request, jsonify, send_from_directory
from .services import get_all_entries, get_active_tasks, get_inactive_tasks, get_random_false_domain, update_false_domain_to_true
from .models import Darkweb, DomainToURL, UrlWeb
import os
from .util.visualize import plot_combined_charts
main = Blueprint('main', __name__)

@main.route('/')
def home():
    entries = get_all_entries()
    return render_template('index.html', entries=entries)

@main.route('/visualize/<int:darkweb_id>')
def visualize_combined(darkweb_id):
    entry = Darkweb.query.get_or_404(darkweb_id)
    words = ' '.join(url.words for url in entry.urls)
    plot_url = plot_combined_charts(words)
    return jsonify({'plot_url': plot_url})


@main.route('/todo')
def todo_onion():
    page_active = int(request.args.get('page_active', 1))
    page_inactive = int(request.args.get('page_inactive', 1))
    items_per_page = 10

    active_list = get_active_tasks(page_active, items_per_page)
    inactive_list = get_inactive_tasks(page_inactive, items_per_page)

    return render_template('TodoOnion.html', 
                           activeList=active_list.items, 
                           numPagesActive=active_list.pages, 
                           pageActive=page_active,
                           inactiveList=inactive_list.items, 
                           numPagesInactive=inactive_list.pages, 
                           pageInactive=page_inactive,
                           totalActive=active_list.total, 
                           totalInactive=inactive_list.total)
@main.route('/api')
def false_domain():
    url_web = get_random_false_domain()
    updated_url_web = update_false_domain_to_true(url_web)
    if updated_url_web:
        return jsonify({'domain': updated_url_web.domain})
    else:
        return jsonify({'error': 'No entries found'}), 404

@main.route('/<path:html_content>')
def crawl_html(html_content):
    print(html_content)
    base_directory = os.path.join(os.path.dirname(__file__), '..','..', 'function')
    
    # 요청된 HTML 파일을 찾기 위해 서비스 기능 폴더 안의 모든 폴더를 검색
    for root, dirs, files in os.walk(base_directory):
        for subdir in dirs:
            html_file_path = os.path.join(root, subdir, f'{html_content}.html')
            if os.path.exists(html_file_path):
                print("hihi")
                return send_from_directory(os.path.join(base_directory, subdir), f'{html_content}.html')
    
    # 해당하는 HTML 파일을 찾지 못한 경우 404 에러 반환
    return 'Not Found', 404
