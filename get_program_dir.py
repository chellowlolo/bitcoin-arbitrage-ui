# Original code by Stephen Gava.
# Retrieved from http://sourceforge.net/mailarchive/forum.php?\
# thread_name=1361064213.15575.YahooMailNeo%40web122902.mail.ne1\
# .yahoo.com&forum_name=cx-freeze-users on 11/8/2013

import os, sys

def get_program_dir():
    """
    return the filesystem directory where the app program file
    resides
    (ie. the applications exec or import directory).
    """
    if hasattr(sys,'frozen'):
        #app is frozen or bundled with py2app or py2exe or cxfreeze
        app_dir=os.path.dirname(sys.executable)
    else:
        if __name__ != '__main__': # we were imported
            app_dir=os.path.dirname(__file__)
        else: # we were exec'ed
            app_dir=os.path.abspath(sys.path[0])
    return app_dir