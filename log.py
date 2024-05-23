from PyQt5.QtWidgets import QApplication, QFileDialog
import logging

# PyQt5 애플리케이션 초기화
app = QApplication([])

# 파일 선택 대화 상자 생성
dialog = QFileDialog()
dialog.setFileMode(QFileDialog.ExistingFiles)  # 폴더 및 파일 선택 모두 허용

# 대화 상자 실행 및 사용자 선택 기다림
if dialog.exec_():
    # 사용자가 선택한 파일 및 폴더 경로 가져오기
    selected_files = dialog.selectedFiles()
    print(selected_files)  # 선택한 파일 및 폴더 출력
    
    # 로그 설정
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='log_analysis.log')

    # 파일 분석 함수
    def analyze_logs(file_path):
        try:
            with open(file_path, 'r') as file:
                logging.info(f"--- Start analysis of {file_path} ---")
                error_count = 0  # 오류 카운트 초기화
                for line_number, line in enumerate(file, start=1):
                    # 로그 분석 작업 수행
                    # 여기에 로그 분석 코드를 추가하세요
                    print(line.strip())  # 예시: 각 줄을 출력
                    # Error 레벨의 로그만 기록
                    if "ERROR" in line:
                        logging.error(line.strip())  # 로그 파일에 로그 기록
                        error_count += 1
                if error_count == 0:
                    logging.info("No errors found in the log file.")
                else:
                    logging.info(f"Identified {error_count} errors in the log file.")
                logging.info("--- End of analysis ---")
        except Exception as e:
            logging.error(f"Error occurred while analyzing logs: {str(e)}")

    # 각 파일에 대해 로그 분석 수행
    for file_path in selected_files:
        analyze_logs(file_path)

# PyQt5 애플리케이션 실행
app.exec_()
