from flask import Flask, request, render_template, send_from_directory, current_app

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('1.html')

@app.route('/', methods=['POST'])
def my_form_post():
    import tabula
    import xlwt
    import pandas as pd


    text = request.form['text']
    processed_text = text.upper()
    file_name = request.form.get('myfile')
    processed_filename = file_name.upper()
    #return  '{} {}'.format(processed_text, processed_filename)

    headers = []
    body = []
    pdf_name = file_name
    df_column = tabula.read_pdf(pdf_name,pages= 'all')[0]
    df = tabula.read_pdf(pdf_name,pages= 'all')

    #print (len(df_column))

    df = tabula.read_pdf(pdf_name,pages= 'all')
    tabula.convert_into(pdf_name, "Converted.csv",pages= 'all')
    #print(df)

    return send_from_directory(current_app.root_path, 'Converted.csv')
    #return 'Coversion successfull'