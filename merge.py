import os

def merge_files(directory, output_file, excluded_files):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py') and file not in excluded_files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, directory)
                    outfile.write(f"\n\n--- {relative_path} ---\n\n")
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())

def main():
    # 현재 작업 디렉토리
    current_directory = os.getcwd()
    
    # 출력 파일 이름
    output_filename = 'projectfiles.txt'
    
    # 제외할 파일 목록을 여기에 정의합니다
    excluded_files = [
        'config.py',
    ]
    
    # 파일 병합 실행
    merge_files(current_directory, output_filename, excluded_files)
    
    print(f"파일 병합이 완료되었습니다. 결과 파일: {output_filename}")
    print(f"현재 작업 디렉토리: {current_directory}")
    print(f"제외된 파일들: {', '.join(excluded_files) if excluded_files else '없음'}")

if __name__ == "__main__":
    main()