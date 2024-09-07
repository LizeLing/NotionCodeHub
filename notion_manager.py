from notion_client import Client
import streamlit as st

NOTION_TOKEN = st.secrets.API_KEY.NOTION_TOKEN
DATABASE_ID = st.secrets.API_KEY.NOTION_DATABASE_ID

notion = Client(auth=NOTION_TOKEN)

TEMPLATES = {
    "Python": ["Python", "JSON"],
    "Web_Basic": ["HTML", "CSS", "JavaScript", "JSON"],
    "Data_Analysis": ["Python", "JSON"],
    "HTML_Single_Page": ["HTML"]
}

def fetch_pages():
    """Notion 데이터베이스에서 페이지를 가져옵니다."""
    try:
        response = notion.databases.query(
            database_id=DATABASE_ID,
            sorts=[{"property": "title", "direction": "ascending"}]
        )
        return response['results']
    except Exception as e:
        st.error(f"Error fetching pages from Notion: {str(e)}")
        raise

def extract_page_content(page_id):
    """Notion 페이지의 내용을 가져옵니다."""
    try:
        response = notion.blocks.children.list(block_id=page_id)
        return response['results']
    except Exception as e:
        st.error(f"Error extracting content for page ID {page_id}: {str(e)}")
        raise

def extract_code_blocks(content, template):
    """페이지 내용에서 코드 블록을 추출합니다."""
    code_blocks = []
    expected_types = TEMPLATES[template]
    current_type_index = 0

    for block in content:
        if block['type'] == 'code' and current_type_index < len(expected_types):
            code_type = expected_types[current_type_index]
            code_content = block['code']['rich_text'][0]['plain_text'] if block['code']['rich_text'] else ""
            code_blocks.append({
                'type': code_type,
                'content': code_content
            })
            current_type_index += 1
    
    return code_blocks

def get_page_icon(page):
    """페이지의 아이콘을 가져옵니다."""
    icon = page.get('icon')
    if icon:
        if icon['type'] == 'emoji':
            return icon['emoji']
        elif icon['type'] == 'external':
            return icon['external']['url']
        elif icon['type'] == 'file':
            return icon['file']['url']
    return '📄'  # 기본 아이콘

def get_all_page_data():
    """모든 페이지 데이터를 가져와 처리합니다."""
    pages = fetch_pages()
    page_data = []
    for page in pages:
        properties = page['properties']
        template = properties['template']['select']['name']
        
        if template not in TEMPLATES:
            continue

        page_data.append({
            'id': page['id'],
            'category': properties['category']['select']['name'],
            'title': properties['title']['title'][0]['plain_text'],
            'template': template,
            'icon': get_page_icon(page)
        })
    
    return page_data

def get_single_page_data(page_id):
    """단일 페이지의 데이터를 가져와 처리합니다."""
    page = notion.pages.retrieve(page_id=page_id)
    properties = page['properties']
    template = properties['template']['select']['name']
    
    if template not in TEMPLATES:
        return None

    content = extract_page_content(page_id)
    codes = extract_code_blocks(content, template)
    
    return {
        'id': page['id'],
        'category': properties['category']['select']['name'],
        'title': properties['title']['title'][0]['plain_text'],
        'template': template,
        'icon': get_page_icon(page),
        'codes': codes
    }