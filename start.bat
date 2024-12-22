@echo off
set "MOVIE_API_KEY=e60f12ebf7f45726de87ac36e81e04d9"
set "SECRET_KEY=4063f0d4acddd7541a283a297037fce064df831dc1111bd2"
set "MAIL_USERNAME=theomarahmedsobhy@gmail.com"
set "MAIL_PASSWORD=eebqjtbikcbaodgt"
set "DATABASE_URL=mysql+pymysql://root:$0bhyk%40b3r@localhost/watchlist"
set "FLASK_APP=manage.py"
set "FLASK_ENV=development"
set "FLASK_CONFIG=development"

call venv\Scripts\activate

REM Run database migrations
flask db upgrade

REM Start the server
python manage.py run
pause
