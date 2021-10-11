#  iMio 2021
#  dmuyshond
#  It's been needed to be certain trace errors are send to admints@imio.be
#  Since it was not automatic and we did not receive important error traces by mail
#  It's now used in our build-e-guichet.sh for newcoming cities
#  More info : https://dev.entrouvert.org/issues/44210
#              https://support.imio.be/browse/TELE-653


from quixote import get_publisher

pub = get_publisher()
pub.reload_cfg()
debug = pub.cfg.get('debug')
if not debug:
    debug = {'error_email': 'admints@imio.be'}
    print(" --- admin TS mail adress has been set-up (mail for error traces).")
else:
    if 'admints' not in debug['error_email']:
        print(" --- Attention, l'adresse admin TS n'est pas set.")
        print("     'error_email' contient ceci : ", debug['error_email'])
pub.cfg['debug'] = debug
pub.write_cfg()
