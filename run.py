import os
import uvicorn
import os
from pathlib import Path
from SMWinservice import SMWinservice
"""
class PythonCornerExample(SMWinservice):
    _svc_name_ = "Passport"
    _svc_display_name_ = "Passport_OCR"
    _svc_description_ = "Use to get Passport Information"

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
"""
		# os.system('uvicorn run_app:app --reload')
		# os.system('''workon passport_ocr
		#             uvicorn run_app_debug:app --reload''')

        os.system("uvicorn run_app_debug:app --reload")
		
"""		
if __name__ == '__main__':
    PythonCornerExample.parse_command_line()
"""