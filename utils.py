from Crypto.Hash import SHA
from Crypto.Random import random
from note import DATA_DIR

def send_email(link, recipient):
    """Send the link via email to a recipient.

    Keyword arguments:
    link -- the random url generated by the application
    recipient -- a valid RFC-compliant email address."""

    import email.utils
    import smtplib
    import time
    from email.mime.text import MIMEText
    msg = MIMEText("%s" % link)
    msg['To'] = email.utils.formataddr(('Self Destructing Notes', recipient))
    msg['From'] = email.utils.formataddr((fullname, fromaddr))
    s = smtplib.SMTP('localhost')
    s.sendmail(fromaddr, [recipient], msg.as_string())
    s.quit()

def duress_text():
    """Return 5 random sentences of the Zen of Python."""
    import subprocess
    text = ''
    p = subprocess.Popen(('python','-c','import this'), stdout=subprocess.PIPE,)
    s = [x for x in p.communicate()[0].splitlines() if x != '']
    for i in range(5):
        text = text + random.choice(s) + ' '
    return text

def verify_hashcash(token):
    """Return True or False based on the Hashcash token

    Valid Hashcash tokens must start with '0000' in the SHA hexdigest string.
    If not, then return False to redirect the user to an error page. If the
    token is valid, but has already been spent, then also return False to
    redirect the user to an error page. Otherwise, if the token is valid and
    has not been spent, append it to the hashcash.db file.

    Keyword arguments:
    token -- a proposed Hashcash token to validate."""

    digest = SHA.new(token)
    with open('%s/hashcash.db' % DATA_DIR, 'a+') as f:
        if digest.hexdigest()[:4] == '0000' and token not in f.read():
            f.write(token+'\n')
            return True
        else:
            return False