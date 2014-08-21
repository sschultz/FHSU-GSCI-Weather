map <Leader>s :!python3 manage.py shell<CR>
map <Leader>r :!python3 manage.py runserver<CR>
map <Leader>d :!python3 manage.py syncdb --noinput<CR>
map <Leader>D :!rm -rf db.sqlite3<CR>:!python3 manage.py syncdb --noinput<CR>
map <Leader>c :!python3 manage.py windfarm --create<CR>
