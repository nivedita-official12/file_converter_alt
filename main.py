from flask import Flask,flash, request, render_template, send_from_directory, current_app,send_file

app = Flask(__name__,static_url_path='/static')
app.secret_key = 'nivi_flask'
@app.route('/')
def my_form():
    return render_template('2.html')

@app.route('/excel_to_pdf', methods=['GET', 'POST'])
def excel_to_pdf():
    if request.method == 'POST':
      if request.form['action'] == "Convert":
        #app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
        file_name = request.form.get('myfile')
        processed_filename = file_name.upper()
        import pandas as pd
        import numpy as np

        df = pd.read_excel('test.xls')

        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template("xlsx_pdf.html")

        column_data = []
        for i in range(0,len(df.head().columns)):
          print (df.head().columns[i])
          column_data.append(df.head().columns[i])
          print (column_data)
          headers = pd.DataFrame(column_data)
          print ('****************************')
          print (len(df))

          pd_code = df['Product_Code'].replace(np.nan,'',regex=True)
          pd_title = df['productTitle'].replace(np.nan,'',regex=True)
          teaser_t = df['teaserText'].replace(np.nan,'',regex=True)
          pd_long_desc = df['productLongDescription'].replace(np.nan,'',regex=True)
          pd_features = df['productFeatures'].replace(np.nan,'',regex=True)
          meta_desc = df['metaDescription'].replace(np.nan,'',regex=True)
          e_240 = df['eCommDescription240'].replace(np.nan,'',regex=True)
          key_wrd = df['keywords'].replace(np.nan,'',regex=True)
          inter_key = df['internalKeyword'].replace(np.nan,'',regex=True)
          un = df['UNSPSC'].replace(np.nan,'',regex=True)
          cnt_auth = df['contentAuthor'].replace(np.nan,'',regex=True)
          inc = df['includes'].replace(np.nan,'',regex=True)
          waran = df['warranty'].replace(np.nan,'',regex=True)
          brnd = df['brand'].replace(np.nan,'',regex=True)
          ft_nt = df['footnotes'].replace(np.nan,'',regex=True)
          comp = df['compliance'].replace(np.nan,'',regex=True)
          crt = df['certifications'].replace(np.nan,'',regex=True)
          dscl = df['disclaimers'].replace(np.nan,'',regex=True)
          al = df['alerts'].replace(np.nan,'',regex=True)
          eu_s = df['EUsupplierName'].replace(np.nan,'',regex=True)
          tf_long = df['TFLongDescription'].replace(np.nan,'',regex=True)
          td_ref = df['techDetailsandRefs'].replace(np.nan,'',regex=True)

          template_vars = {"header_list":headers,"pivot_table": df.to_html(),"len":len(df),
          "p_code":pd_code,"p_title":pd_title,"teas_t":teaser_t,"p_lng_desc":pd_long_desc,
          "p_features":pd_features,"meta_d":meta_desc,"e_desc_240":e_240,"kw":key_wrd,
          "inter_ky_wrd":inter_key,"unc":un,"cont_author":cnt_auth,"incd":inc,"warant":waran,
          "bran":brnd,"foot_nt":ft_nt,"compl":comp,"certi":crt,"dsclm":dscl,"alrt":al,
          "eu_supp":eu_s,"tf_lng":tf_long,"tech_det": td_ref}

          html_out = template.render(template_vars)

          from weasyprint import HTML
          HTML(string=html_out).write_pdf("report.pdf")
          final_output = 'Covertion is Completed'
          return render_template('3.html',predict_content=final_output)

    return render_template('3.html')
    
    if request.form['action'] == "Download":
      path = "report.pdf"
      return send_file(path, as_attachment=True)

@app.route('/pdf_to_excel', methods=['GET', 'POST'])
def pdf_to_excel():
    if request.method == 'POST':
        import tabula
        import xlwt
        import pandas as pd

        file_name = request.form.get('myfile')
        processed_filename = file_name.upper()
        
        headers = []
        body = []
        pdf_name = file_name
        df_column = tabula.read_pdf(pdf_name,pages= 'all')[0]
        df = tabula.read_pdf(pdf_name,pages= 'all')
        df = tabula.read_pdf(pdf_name,pages= 'all')
        tabula.convert_into(pdf_name, "Converted.csv",pages= 'all')
        #return send_from_directory(current_app.root_path, 'Converted.csv')
        return 'Data Convertion Done Successfully'
    
    return render_template('4.html')

@app.route('/pdf_extraction', methods=['GET', 'POST'])
def pdf_extraction():
    if request.method == 'POST':
        from PyPDF2 import PdfFileWriter, PdfFileReader
        file_name = request.form.get('myfile')
        start = request.form.get('start_point')
        end = request.form.get('end_point')
        
        inputpdf = PdfFileReader(open(file_name, "rb"))
        start_page = int(start)
        end_page = int(end)
        for i in range(start_page,end_page+1):
            output = PdfFileWriter()
            output.addPage(inputpdf.getPage(i))
            with open("document-page%s.pdf" % i, "wb") as outputStream:
                output.write(outputStream)


        #return send_from_directory(current_app.root_path, 'Converted.csv')
        return 'Data Extraction Done Successfully'
    
    return render_template('5.html')