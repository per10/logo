import flask
import os
import re
from PIL import Image

app = flask.Flask(__name__)


"""
    This python script can be used to scale a logo for presentation on a web page.
    It needs a base image, logo.jpg, and will scale this, while keeping the aspect
    ratio to a required width. The request from the web server should look like this:

    /logo_200.jpg

    The script will start looking if there is already a file generated. If not it
    will generate it and send it back. There is also a limitatino on how much it
    can be scaled, currently from 10px to 1000px.

"""
@app.route('/<logo_file>')
def hello_world(logo_file=None):

    if re.search("^logo_\d\d+\.jpg$", logo_file) == None:
        return "Wrong path"
    else:
        logo_size = re.search("\d+", logo_file).group(0)
        if int(logo_size) < 10 or int(logo_size) > 1000:
            return "Wrong size"

    if os.path.isfile(os.environ['HOME'] + '/img/' + logo_file):
        pass
    else:
        img = Image.open('logo.jpg')
        wpercent = (int(logo_size) / float(img.size[0]))
        hsize = int((float(img.size[1] * float(wpercent))))
        img = img.resize((int(logo_size), hsize), Image.ANTIALIAS)
        img.save(os.environ['HOME'] + '/img/' + logo_file)
    
    return flask.send_file(os.environ['HOME'] + '/img/' + logo_file,
      mimetype='image/jpg')
