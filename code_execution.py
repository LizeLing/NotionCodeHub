import io
import sys
import json
from contextlib import redirect_stdout
import streamlit as st

def execute_code(code, json_data):
    """코드를 실행하고 출력을 반환합니다. JSON 데이터가 제공되면 이를 포함합니다."""
    output = io.StringIO()
    with redirect_stdout(output):
        try:
            if json_data and json_data.strip():
                try:
                    json_obj = json.loads(json_data)
                    exec(f"data = {json.dumps(json_obj)}\n{code}")
                except json.JSONDecodeError:
                    print("Warning: Invalid JSON data. Executing code with empty JSON.")
                    exec(f"data = {{}}\n{code}")
            else:
                print("Note: JSON data is empty. Executing code with empty JSON.")
                exec(f"data = {{}}\n{code}")
        except Exception as e:
            print(f"Error executing code: {str(e)}")
    result = output.getvalue()
    return result

def execute_web_code(html_code, css_code, js_code, json_code):
    """HTML, CSS, JavaScript, JSON 코드를 통합하여 실행합니다."""
    integrated_html = html_code
    if css_code:
        integrated_html = integrated_html.replace('</head>', f'<style>{css_code}</style></head>')
    if js_code:
        integrated_html = integrated_html.replace('</body>', f'<script>{js_code}</script></body>')
    
    # JSON 데이터 처리
    if json_code and json_code.strip():
        try:
            json.loads(json_code)  # JSON 유효성 검사
            integrated_html = integrated_html.replace('</body>', f'<script>var data = {json_code};</script></body>')
        except json.JSONDecodeError:
            st.warning("Invalid JSON data. Web page will include empty JSON data.")
            integrated_html = integrated_html.replace('</body>', '<script>var data = {};</script></body>')
    else:
        st.info("JSON data is empty. Web page will include empty JSON data.")
        integrated_html = integrated_html.replace('</body>', '<script>var data = {};</script></body>')
    
    return integrated_html