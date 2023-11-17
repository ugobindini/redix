# redix
ReDiX - Renaissance Digital eXplorer. A website for sound analysis in polyphonic music of the Renaissance.

The database is the union of the scores available thanks to the [Josquin Research Project](https://josquin.stanford.edu)

# Requisites
`python3` with its module `Django` (version 4); `humdrum-tools' available on github at https://github.com/humdrum-tools/humdrum-tools.

# Install and usage

Download the project

`git clone https://github.com/ugobindini/redix`

Move to the newly created folder 'redix'

`cd redix`

Launch the server

`python3 manage.py runserver`

Go to the webpage http://127.0.0.1:8000/fb.

# Known bugs
The musical snippets of Du Fay's Missa L'homme armé cannot be displayed on the webpage, due to an error of the humdrum-tool command myank (trying to fix it with the developer).
