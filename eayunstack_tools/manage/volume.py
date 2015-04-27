#volume management
import logging
import os
import commands

LOG = logging.getLogger(__name__)

env_path = os.environ['HOME'] + '/openrc'

def volume(parser):
    print "reference module"
    if parser.DESTROY_VOLUME:
        if not parser.ID:
            LOG.error('Please use [--id ID] to specify the volume ID !')
        else:
            volume_id = parser.ID
            global volume_id
            destroy_volume()

def make(parser):
    '''Volume Management'''
    parser.add_argument(
        '-l',
        '--list-errors',
        action='store_const',
        const='list_errors',
        help='List Error Volumes'
    )
    parser.add_argument(
        '-d',
        '--destroy-volume',
        dest='DESTROY_VOLUME',
        action='store_true',
        default=False,
        help='Destroy Volume'
    )
    parser.add_argument(
        '--id',
        action='store',
        dest='ID',
        help='Volume ID'
    )
    parser.set_defaults(func=volume)

def list_errors():
    print "List Error Volume"

def destroy_volume():
    print "Destroy Error Volume: %s" % volume_id
    # get volume's info
    (s, o) = commands.getstatusoutput('source %s && cinder show %s' % (env_path, volume_id))
    if s != 0 or o is None:
        LOG.error('Can not find this volume !')
        return
    else:
        status = get_volume_value(o, 'status')
        volume_type = get_volume_value(o, 'volume_type')
        attachments = get_volume_value(o, 'attachments')

    if not determine_volume_status(status):
        LOG.warn('User give up to destroy this volume.')
        return
    else:
        print 'destroy volume %s' % volume_id

def determine_volume_status(status):
    if status in ['available','creating','deleting','error_deleting','attaching','detaching']:
        while True:
            status_determine = raw_input('This volume in "%s" status, do you really want to destroy it? [yes/no]: ' % status)
            if status_determine in ['yes','no']:
                break
        if status_determine == 'yes':
            return True
        else:
            return False
    else:
        return True

def get_volume_value(info, key):
    for entry in info.split('\n'):
        if len(entry.split('|')) > 1:
            if entry.split('|')[1].strip() == key:
                return entry.split('|')[2].strip()
