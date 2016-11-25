import cherrypy
import os
from CBMDriver import *
from ParaProc import *
from cherrypy import response
from functools import wraps
import simplejson
import uuid
from bs4 import BeautifulSoup

MEDIA_DIR = os.path.join(os.path.abspath("."), "media")

cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 8080,
                        'tools.sessions.on': True,
                        'tools.sessions.timeout':60
                       })
cherrypy.engine.restart()

config = {'/media':
   {'tools.staticdir.on': True,
   'tools.staticdir.dir': MEDIA_DIR,}
}

class TutorHome(object):
    @cherrypy.expose
    def index(self):
        if 'count' not in cherrypy.session:
            cherrypy.session['count'] = 0
        cherrypy.session['count'] += 1
        return open(os.path.join(MEDIA_DIR, u'home.html'))
    @cherrypy.expose
    def ParseInput(self, ModeSet, KeigoString):
        p = ParagraphPreprocessor()
        RPage = open(os.path.join(MEDIA_DIR, u'result.html'))
        output=""
        #Preprocess the submitted string. We pass it to the engine sentence-by-sentence.
        p.MarkExpressions(KeigoString.strip(),ModeSet)
        SessionId = str(uuid.uuid4())
        cherrypy.session['map'+SessionId] = p.pkMap
        for sentence in p.MarkedSentences:
            output+=sentence
        soup = BeautifulSoup(RPage.read(),"lxml")
        ParsedStr = soup.find("div",id="ParsedString")
        ParsedStr.insert(0,output)
        resultPage = str(soup.prettify(formatter=None))
        resultPage = resultPage.replace("ModeSetEditable", ModeSet)
        resultPage = resultPage.replace("SessionId", '"'+SessionId+'"')
        return (resultPage)
    
    @cherrypy.expose()
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def ConstraintCheck(self):
        response.headers["Content-Type"] = "application/json"
        json_response = cherrypy.request.json
        pkMap = cherrypy.session.get('map'+json_response["sid"])
        x = CBMDriver(pkMap[json_response["pk"]],json_response["value"],json_response["mode"])
        if x.Verify():
            return simplejson.dumps({'pk':json_response["pk"],
                                     'IsCorrect':1,
                                     'msg': "Correct"
                                     })
        else:
            return simplejson.dumps({'pk':json_response["pk"],
                                     'IsCorrect':0,
                                     'msg': ', '.join(x.ShowAnswer())
                                     })

cherrypy.tree.mount(TutorHome(), '/', config=config)
cherrypy.engine.start()
#cherrypy.engine.timeout_monitor.unsubscribe()
#cherrypy.server.socket_timeout = 0
