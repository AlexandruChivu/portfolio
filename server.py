from flask import Flask, render_template, request, url_for, redirect, jsonify, send_from_directory
import os, csv

# Determine the directory of server.py
script_dir = os.path.dirname(__file__)

# Create a relative path to database.txt
database_path = os.path.join(script_dir, 'database.csv')

# Define the directory where downloadable files are stored
downloadable_files_dir = os.path.join(script_dir, 'CV')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

# Create a route for downloading the PDF
@app.route('/download_pdf')
def download_pdf():
    pdf_filename = "Chivu-Alexandru.pdf"  # The name of the PDF file
    return send_from_directory(downloadable_files_dir, pdf_filename, as_attachment=True)

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.get_json()  # Get JSON data from the request
            name = data["name"]
            email = data["email"]
            message = data["message"]

            # Write the data to the file
            with open(database_path, mode='a', newline='') as database:
                csv_writer = csv.writer(database)

                # Check if the file is empty, and if so, write the header
                if os.path.getsize(database_path) == 0:
                    csv_writer.writerow(["name", "email", "message"])
                
                csv_writer.writerow([name,email,message])

            return jsonify({"message": "Data successfully submitted"})
        except Exception as e:
            return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
