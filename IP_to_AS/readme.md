
`Liệt kê các phụ thuộc của python`
pip freeze > requirements.txt
hoặc 
pip install pipreqs
pipreqs /path/to/your/python/project


`Chạy lệnh sau để build thành app`
pyinstaller --onefile --noconsole app.py
pyinstaller --onefile --requirement requirements.txt --noconsole app.py

