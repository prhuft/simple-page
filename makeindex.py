#### generate the index.html files
import os

files = [f for f in os.listdir('.') if 
         (os.path.isfile(f) and f[-4:]=='html' and 'index' not in f)]
for idx in version_idxs:
    with open("index"+ idx +".html", 'w') as f:
        text = f"""<html>
             <body>   
             <h1>Welcome to my webpage (version={idx})</h1>
             <p>Directory <br /> \n"""
        for file in files:
            if 'donate' in file:
                text += f"<a href = '{file}?from={idx}'>{file[:-5]}</a><br /> \n"
            else: # could use a regex insertion here instead?
                text += f"<a href = '{file}'>{file[:-5]}</a><br /> \n"     
        text += "</p> \t \n</body>\n</html>"
        f.write(text)