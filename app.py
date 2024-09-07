import streamlit as st
import json
from notion_manager import get_all_page_data, get_single_page_data
from code_execution import execute_code, execute_web_code
from utils import group_pages_by_category, initialize_session_state, get_sorted_categories, get_html_download_link

def main():
    st.set_page_config(
        layout="wide", 
        page_title="📝Notion Code Hub",
        page_icon="https://upload.wikimedia.org/wikipedia/commons/4/45/Notion_app_logo.png"
    )
    
    # Streamlit 컴포넌트의 기본 스타일을 제거하는 CSS
    st.markdown("""
        <style>
        iframe {
            border: none !important;
            box-shadow: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("📝Notion Code Hub")
    
    st.info("노션 코드 허브에 오신것을 환영합니다! 🎉\n")

    try:
        if 'page_data' not in st.session_state:
            st.session_state.page_data = get_all_page_data()

        grouped_pages = group_pages_by_category(st.session_state.page_data)
        sorted_categories = get_sorted_categories(grouped_pages)

        st.sidebar.title("카테고리")

        if not initialize_session_state(grouped_pages):
            return

        # 카테고리와 페이지 선택을 위한 UI
        for category in sorted_categories:
            with st.sidebar.expander(category):
                for page in grouped_pages[category]:
                    if st.button(f"{page['icon']} {page['title']}", key=f"btn_{page['id']}", use_container_width=True):
                        st.session_state.selected_category = category
                        st.session_state.selected_page = page['title']
                        st.session_state.selected_page_data = get_single_page_data(page['id'])
                        if 'generated_html' in st.session_state:
                            del st.session_state.generated_html
                        if 'html_display' in st.session_state:
                            del st.session_state.html_display

        # 선택된 페이지 내용 표시
        if 'selected_page_data' in st.session_state and st.session_state.selected_page_data:
            selected_page = st.session_state.selected_page_data
            st.header(f"{selected_page['icon']} {selected_page['title']}")
            
            # 코드 실행 버튼 표시
            if selected_page['codes']:
                if selected_page['template'] in ['Web_Basic', 'HTML_Single_Page']:
                    html_code = next((code['content'] for code in selected_page['codes'] if code['type'] == 'HTML'), '')
                    css_code = next((code['content'] for code in selected_page['codes'] if code['type'] == 'CSS'), '')
                    js_code = next((code['content'] for code in selected_page['codes'] if code['type'] == 'JavaScript'), '')
                    json_code = next((code['content'] for code in selected_page['codes'] if code['type'] == 'JSON'), '')
                    
                    if st.button("Generate and Run Code"):
                        if selected_page['template'] == 'Web_Basic':
                            integrated_html = execute_web_code(html_code, css_code, js_code, json_code)
                        else:
                            integrated_html = html_code
                        st.session_state.generated_html = integrated_html
                        st.session_state.html_display = f'<div style="height: 600px; overflow-y: scroll;">{integrated_html}</div>'
                    
                    if 'html_display' in st.session_state:
                        st.components.v1.html(st.session_state.html_display, height=620)
                    
                    if 'generated_html' in st.session_state:
                        st.download_button(
                            label="Download HTML",
                            data=st.session_state.generated_html,
                            file_name=f"{selected_page['title']}.html",
                            mime="text/html",
                        )
                
                elif selected_page['template'] in ['Python', 'Data_Analysis']:
                    python_code = next((code['content'] for code in selected_page['codes'] if code['type'] == 'Python'), None)
                    json_code = next((code['content'] for code in selected_page['codes'] if code['type'] == 'JSON'), '')
                    
                    if python_code:
                        if st.button("Run Python Code"):
                            if json_code and json_code.strip():
                                st.info("Executing Python code with JSON data.")

                            output = execute_code(python_code, json_code)
                            st.text_area("Execution Result:", value=output, height=400)
                    
                    if json_code:
                        st.subheader("JSON Data")
                        if json_code.strip():
                            try:
                                json.loads(json_code)  # JSON 유효성 검사
                                st.json(json.loads(json_code))
                            except json.JSONDecodeError:
                                st.error("Error: Invalid JSON data. This may affect code execution.")
                        else:
                            st.info("JSON data is empty.")
            else:
                st.info(f"No executable code provided for this page (Template: {selected_page['template']}).")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please check your Notion database and ensure it contains valid pages and code blocks.")

if __name__ == "__main__":
    main()