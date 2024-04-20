# py_interactive_dashboard


## Package requirements

Install package requirements

```
pip install -r requirements.txt
```

Untuk install ulang requirements **panel**, lakukan instalasi berikut
```
pip install -r requirements_panel.txt
```


## How to run

Jika muncul url pada console, buka url tersebut untuk melihat dashboard

* Streamlit

```
streamlit run dashboard_streamlit.py
```

https://github.com/m-fariz-a/py_interactive_dashboard/assets/73702296/c8530968-0929-429c-b842-0e1b60b2016c


* Dash

```
python dashboard_dash.py
```

* Shiny

```
shiny run --reload --launch-browser dashboard_shiny.py
```

https://github.com/m-fariz-a/py_interactive_dashboard/assets/73702296/5143786f-1019-4480-b0d0-8b798f259196


* Panel

```
Visual Studio Code (VS Code) supports notebooks and ipywidgets, and Panel objects can be used as ipywidgets thanks to **jupyter_bokeh**, which means that you can use Panel components interactively in VS Code. Ensure you install **jupyter_bokeh** with **pip install jupyter_bokeh** or **conda install -c bokeh jupyter_bokeh** and then enable the extension with **pn.extension()**.
```


If you prefer developing in a Python Script using an editor, you can copy the code into a file app.py and serve it.

```
panel serve dashboard_panel.py --autoreload
```

https://github.com/m-fariz-a/py_interactive_dashboard/assets/73702296/93d480d1-ad79-46b2-9142-abbaafd5233a
