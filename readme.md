
Install requirement: <br />
````shell
$ pip install psycopg2-binary
$ pip install pyaudio
$ pip install PyQt6
$ pip install PySide6
$ pip install matplotlib
````
Run: 
````shell
$ python srg.py
````
1 - start mic stream <br />
2 - graph(spectrum & FFT) and play <br />
3 - save to postgresql (DB=sound, user=python, pass=python, table=storage) <br />
4 - get from postgresql <br />
5 - graph and play <br />
