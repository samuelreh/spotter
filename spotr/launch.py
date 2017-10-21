from .pricing import get_az
from .spot_instance import request
from .instance import tag as tag_instance
from .instance import get_by_instance_id
from .client import build as build_client
from .config import Config
from .key import find_or_create as find_or_create_key


def launch(args):
    client = build_client(args)
    conf = Config(client, args)

    key_path = find_or_create_key(client, conf.key_name)

    az = get_az(client, conf)
    _log_launching(az)
    conf.set_az(az.zone_name)

    inst = request(client, conf, tag_instance, get_by_instance_id)
    _log_instance_creation(inst, key_path)
    return inst


def _log_launching(az):
    print(">> Launching instance in:")
    print(str(az))


def _log_instance_creation(instance, key_path):
    print(">> Instance launched, connect with:")
    ip = str(instance.ip_address)
    print("ssh -i " + key_path + " ubuntu@" + ip)
