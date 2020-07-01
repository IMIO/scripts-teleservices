#  iMio 2020
#  dmuyshond
#  It's been needed to be certain trace errors are send to admints@imio.be
#  Since it was not automatic and we did not receive important error traces by mail
#  It's now used in our build-e-guichet.sh for newcoming cities
#  More info : https://dev.entrouvert.org/issues/44210


from quixote import get_publisher

pub = get_publisher()
pub.reload_cfg()
debug = pub.cfg.get('debug')
if not debug:
    debug = {'error_email': 'admints@imio.be'}
else:
    debug['error_email'] = 'admints@imio.be'
pub.cfg['debug'] = debug
pub.write_cfg()
