import streamlit as st
import base64

def group_pages_by_category(page_data):
    """페이지를 카테고리별로 그룹화합니다."""
    grouped_pages = {}
    for page in page_data:
        if page['category'] not in grouped_pages:
            grouped_pages[page['category']] = []
        grouped_pages[page['category']].append(page)
    return grouped_pages

def get_sorted_categories(grouped_pages):
    """카테고리를 알파벳 순서로 정렬하여 반환합니다."""
    return sorted(grouped_pages.keys())

def initialize_session_state(grouped_pages):
    """세션 상태를 초기화합니다."""
    sorted_categories = get_sorted_categories(grouped_pages)
    
    if not grouped_pages:
        st.error("No pages found in the database. Please check your Notion setup.")
        return False

    if 'selected_category' not in st.session_state or st.session_state.selected_category not in grouped_pages:
        st.session_state.selected_category = sorted_categories[0]
    
    if 'selected_page' not in st.session_state or not grouped_pages[st.session_state.selected_category]:
        if grouped_pages[st.session_state.selected_category]:
            st.session_state.selected_page = grouped_pages[st.session_state.selected_category][0]['title']
        else:
            st.error(f"No pages found in the category: {st.session_state.selected_category}")
            return False

    return True

def get_html_download_link(html_string, filename="download.html"):
    """HTML 문자열을 다운로드 가능한 링크로 변환합니다."""
    b64 = base64.b64encode(html_string.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="{filename}">Download HTML file</a>'
    return href