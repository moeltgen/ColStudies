"""
    ColStudies application settings
    
    You may enter usernames and passwords to simplify usage
    If you leave this empty, login information will be prompted for 
    
"""




#settings for the colectica api
colecticahostname = 'svko-colectica1.gesis.intra'
colecticausername = ''
colecticapassword = ''

#settings for the da|ra api
daraapi = 'https://labs.da-ra.de/dara/study/importXML'
darausername = ''
darapassword = ''
daradoiprefix = '' #will override Colectica metadata, e.g. for test prefix. Empty string if not used.

#settings for DBKEdit
dbkediturl = 'http://dbkedit-server.gesis.intranet/dbkediturl/'
dbkeditusername = ''
dbkeditpassword = ''

#settings for STAR File Storage
starpath = 'N:\\Networkdrive\\Networkfolder\\folder'
