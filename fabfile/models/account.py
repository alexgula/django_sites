# coding=utf-8
import socket, yaml
from fabric.api import env
from ..util import path, serial, fs

account_cache = {}


def load_account(name):
    """Generate account config object from configuration file."""
    if not account_cache.has_key(name):
        with open(path.account_config(name), 'r') as file:
            account_cache[name] = Account(name, serial.for_file(file.name), **yaml.load(file))
    return account_cache[name]


def list_accounts(*args):
    if args:
        for account in args:
            yield account
    else:
        for account in fs.list_local_files(env.local_config_dir, '.yaml'):
            yield account


def safe_list(value):
    """Create safe list."""
    if value is None:
        return []
    elif isinstance(value, (basestring, dict)):
        return [value]
    else:
        return value


def safe_dict(value):
    """Create safe dict."""
    if value is None:
        return {}
    elif isinstance(value, dict):
        return value
    else:
        raise TypeError("safe_dict got unexpected argument - {}".format(value))


def is_valid_ip(value):
    try:
        socket.inet_aton(value)
        return True
    except (socket.error, TypeError):
        return False


def host_name(acc_name, host_name):
    return '_'.join([acc_name, host_name]) if host_name else acc_name


def host_domain(host_name, domain):
    return '.'.join([host_name, domain]) if host_name else domain


def host_path(host_name):
    return '/' + host_name if host_name else ''


def split_cname(cname, default):
    values = cname.split(' ', 1)
    if len(values) < 2:
        return cname, default
    else:
        return values[0].strip(), values[1].strip()


def domain_redirect(domain_from, domain_to):
    if domain_from == domain_to:
        return ['www.' + domain_from], domain_to
    else:
        return ['www.' + domain_from, domain_from], domain_to


class EmptyAddressException(Exception):
    pass


class Domain(object):
    def __init__(self, account, name, generate=True, address=None, mail=None, gmail_dkim=None, hotmail_mx=None,
                 cname=None, txt=None, mx=None, subdomains=None):
        self.account = account
        self.name = name
        self.generate = generate
        self.address = account.address_to_ip(address)
        self.mail = account.address_to_ip(mail) if mail is not None and mail not in (
            'gmail', 'hotmail', 'local') else mail
        self.gmail_dkim = gmail_dkim
        self.hotmail_mx = hotmail_mx
        self.cname = [split_cname(name, self.name) for name in safe_list(cname)]
        self.txt = safe_list(txt)
        self.mx = safe_list(mx)
        self.subdomains = safe_dict(subdomains)

        for name, address in self.subdomains.iteritems():
            self.subdomains[name] = account.address_to_ip(address, self.address)


class Host(object):
    def __init__(self, account, name, enabled=True, generate=True, system=None, address=None, domains=None, primary_domain=None,
                 mysql=None, pgsql=None, project=None, **kwargs):
        self.account = account
        self.name = name or account.name
        self.full_name = host_name(account.name, name)
        self.enabled = enabled
        self.generate = generate
        self.path = host_path(name)
        self.system = account.value('system', system)
        self.address = account.address_to_ip(address)
        self.mysql = account.value('mysql', mysql)
        self.pgsql = account.value('pgsql', pgsql)
        self.project = project or self.name # Override host name for Django
        self.kwargs = kwargs

        if domains:
            self.domains = safe_list(domains)
        else:
            self.domains = [host_domain(name, domain) for domain in account.domains_with_address(self.address)]

        if primary_domain is None:
            self.redirects = [domain_redirect(domain, domain) for domain in self.domains]
            self.primary_domains = self.domains
        else:
            self.redirects = [domain_redirect(domain, primary_domain) for domain in self.domains]
            self.primary_domains = [primary_domain]

    def __getattr__(self, name):
        return self.kwargs[name]


class Account(object):
    def __init__(self, name, serial, system=None, address=None, enabled=True, domains=None, hosts=None, **kwargs):
        self.name = name
        self.serial = serial
        self.zone_email = env.zone_email
        self.enabled = enabled
        self.defaults = {
            'system': system,
            'address': address if is_valid_ip(address) else env.addresses[address],
            'mysql': self.db_list(kwargs, 'mysql'),
            'pgsql': self.db_list(kwargs, 'pgsql'),
        }

        self.domains = [Domain(self, **safe_dict(domain)) for domain in domains] if domains is not None else []

        if not hosts:
            hosts = {'': {}}
        self.hosts = [Host(self, name, **safe_dict(host)) for name, host in hosts.iteritems()]

    def get_hosts(self, server):
        address = self.address_to_ip(server)
        return (host for host in self.hosts if host.enabled and host.address == address)

    def address_to_ip(self, param, default=None):
        if param is None:
            if default is None:
                if self.defaults['address'] is None:
                    raise EmptyAddressException()
                else:
                    return self.defaults['address']
            else:
                return default
        elif is_valid_ip(param):
            return param

        return env.addresses[param]

    def db_list(self, kwargs, db_type):
        """Make database list from kwargs (note lack of **, it's just a dictionary parameter) of database type.

        If key is not in kwargs, it means we don't have any database of this type.
        If key is in kwargs, we have at least one database of this type. If value is empty, create default database."""
        if not db_type in kwargs:
            return None
        names = safe_list(kwargs[db_type] or '')
        return [host_name(self.name, name) for name in names]

    def value(self, name, value):
        return value or self.defaults[name]

    def domains_with_address(self, address):
        return [domain.name for domain in self.domains if domain.address == address]
