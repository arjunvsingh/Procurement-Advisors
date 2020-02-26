from flask import Flask, make_response, request, send_file
import pandas as pd
from fuzzywuzzy import fuzz

app = Flask(__name__)

def transform(files):
    currentFileName = files.filename[:-4]
    database = pd.read_excel("/home/arjunvsingh/mysite/vendorDB.xlsx")
    df = pd.read_csv(files)

    df['Vendor Match'] = ''
    df['Score'] = 0
    df['Vendor'] = df['Vendor'].str.lower()
    for j in range(0,len(df)):
        bestScore = 0
        bestVendor = ''
        for i in range(0,len(database)):
            currScore = fuzz.token_sort_ratio(df['Vendor'][j], str.lower(database['Standard Vendor'][i]))
            if currScore >= bestScore and currScore > 20:
                bestScore = currScore
                bestVendor = database['Standard Vendor'][i]
        df['Vendor Match'][j] = bestVendor
        df['Score'][j] = bestScore


    df.to_csv("/home/arjunvsingh/mysite/uploads/" + currentFileName + '.csv')
    return send_file("/home/arjunvsingh/mysite/uploads/"+ currentFileName + '.csv', attachment_filename=currentFileName + '.csv')

@app.route('/', methods=["POST","GET"])
def form():
    return """
        <html>
            <body>
                <h1 align="center">Vendor Normalization</h1>
                <h2 align="center">Use this tool to normailze vendor names in your AP data. Please use the following template before uploading your file:<h2>

                <form align="center" action="/format" method="post" enctype="multipart/form-data">
                    <input type="submit" value="Download Template">
                </form>

                <h2 align="center">Upload your file below<h2>
                <form align="center" action="/transform" method="post" enctype="multipart/form-data">
                    <input type="file" name="data_file" />
                    <input type="submit" />
                </form>
            </body>
        </html>
    """

@app.route('/transform', methods=["POST"])
def transform_view():
    request_file = request.files['data_file']
    if not request_file:
        return "No file"

    # file_contents = request_file.stream.read().decode("utf-8")

    result = transform(request_file)

    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    return response

@app.route('/format', methods=["POST"])
def APformat():
    response = make_response(send_file("/home/arjunvsingh/mysite/templates/APtemplate.csv", attachment_filename="APtemplate.csv"))
    response.headers["Content-Disposition"] = "attachment; filename=template.csv"
    return response