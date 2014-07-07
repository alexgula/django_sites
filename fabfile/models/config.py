# coding=utf-8
import os
from jinja2 import Environment, FileSystemLoader
from fabric.api import env
from ..util import serial, path, fs
from .account import load_account, list_accounts

def generate_content(template, context, output_path):
    content = template.render(context)
    fs.ensure_local_dir(os.path.split(output_path)[0])
    with open(output_path, 'w') as f:
        f.write(content)

jinja_env = None

def get_template(name):
    global jinja_env
    if jinja_env is None:
        jinja_env = Environment(loader=FileSystemLoader(env.local_template_dir))
    return jinja_env.get_template(name + '.jinja2')


class Config(object):

    def __init__(self, name):
        self.name = name

    def get_etc_parts(self):
        raise TypeError("Absract class instantiated")

    def get_etc_local(self):
        raise TypeError("Absract class instantiated")

    def get_etc_remote(self):
        raise TypeError("Absract class instantiated")

    def get_context(self):
        return {
            'env': env,
        }


class GeneratorMixin(object):

    @property
    def template(self):
        return get_template(self.get_template_name())

    def get_template_name(self):
        raise TypeError("Absract class instantiated")

    def enabled(self):
        return True

    def generate_config(self):
        context = self.get_context()
        generate_content(self.template, context, self.get_etc_local())
        return self.get_etc_local(), self.get_etc_remote()


class ServiceConfig(Config):

    def __init__(self, server, name, service_name=None, etc_name=None):
        super(ServiceConfig, self).__init__(name=name)
        self.server = server
        self.service_name = service_name or name
        self.etc_name = etc_name or name

    def get_etc_local(self):
        return path.etc_local(self.server, self.etc_name, *self.get_etc_parts())

    def get_etc_remote(self):
        return path.etc(self.etc_name, *self.get_etc_parts())

    def generate_account_config(self, account):
        raise TypeError("Absract class instantiated")

    def generate(self, *args):
        for account_name in list_accounts(*args):
            account = load_account(account_name)
            if account.enabled:
                for result in self.generate_account_config(account):
                    yield result


class WebServiceConfig(ServiceConfig):

    def __init__(self, port, server, name, service_name=None, etc_name=None):
        super(WebServiceConfig, self).__init__(server=server, name=name, service_name=service_name, etc_name=etc_name)
        self.port = port

    def get_context(self):
        context = super(WebServiceConfig, self).get_context()
        context['port'] = self.port
        return context

    def generate_account_config(self, account):
        config = AccountConfig(self, account)
        if config.enabled():
            yield config.generate_config()


class ApacheServiceConfig(WebServiceConfig):

    def generate_account_config(self, account):
        config = ApacheConfig(self, account)
        if config.enabled():
            yield config.generate_config()


class NginxServiceConfig(WebServiceConfig):

    def get_context(self):
        context = super(NginxServiceConfig, self).get_context()
        context['backend_port'] = env.service_handlers['a'].port
        return context


class UwsgiServiceConfig(WebServiceConfig):

    def generate_account_config(self, account):
        for host in account.get_hosts(self.server):
            config = UwsgiProjectConfig(self, host)
            if config.enabled():
                yield config.generate_config()


class BindZoneConfig(ServiceConfig, GeneratorMixin):

    def get_template_name(self):
        return self.etc_name + '_zone'

    def get_etc_parts(self):
        return 'named.conf.local',

    def get_context(self):
        context = super(BindZoneConfig, self).get_context()
        domains = []
        for account_name in list_accounts():
            account = load_account(account_name)
            for domain in account.domains:
                config = BindDomainConfig(self, domain)
                if config.enabled():
                    domains.append((domain, config.get_etc_remote()))
        context['domains'] = domains
        return context

    def generate_account_config(self, account):
        for domain in account.domains:
            config = BindDomainConfig(self, domain)
            if config.enabled():
                yield config.generate_config()

    def generate(self, *args):
        for result in super(BindZoneConfig, self).generate(*args):
            yield result
        yield self.generate_config()


class SiteConfig(Config, GeneratorMixin):

    def __init__(self, service):
        super(SiteConfig, self).__init__(name=service.name)
        self.service = service

    def get_context(self):
        context = super(SiteConfig, self).get_context()
        context.update(self.service.get_context())
        return context

    def get_etc_local(self):
        return path.etc_local(self.service.server, self.service.etc_name, *self.get_etc_parts())

    def get_etc_remote(self):
        return path.etc(self.service.etc_name, *self.get_etc_parts())


class AccountConfig(SiteConfig):

    def __init__(self, service, account):
        super(AccountConfig, self).__init__(service=service)
        self.account = account

    def get_template_name(self):
        return self.service.name + '_account'

    def get_etc_parts(self):
        return 'sites-enabled', self.account.name + '.conf'

    def get_context(self):
        context = super(AccountConfig, self).get_context()
        context['hosts'] = self.account.get_hosts(self.service.server)
        context['user'] = self.account.name
        context['root'] = path.account(self.account.name)
        return context

    def enabled(self):
        current_server_hosts = [host for host in self.account.get_hosts(self.service.server)]
        return self.account.enabled and current_server_hosts


class ApacheConfig(AccountConfig):

    def enabled(self):
        php_host_systems = [host.system != 'django' for host in self.account.get_hosts(self.service.server)]
        return super(ApacheConfig, self).enabled() and php_host_systems and any(php_host_systems)


class UwsgiProjectConfig(SiteConfig):

    def __init__(self, service, host):
        super(UwsgiProjectConfig, self).__init__(service=service)
        self.host = host

    def get_template_name(self):
        return self.service.name + '_project'

    def get_etc_parts(self):
        return 'vassals', self.host.name + '.ini'

    def get_context(self):
        context = super(UwsgiProjectConfig, self).get_context()
        context['host'] = self.host
        context['root'] = path.django_site(self.host.project)
        return context

    def enabled(self):
        return super(UwsgiProjectConfig, self).enabled() and self.host.system == 'django'


class BindDomainConfig(SiteConfig):

    def __init__(self, service, domain):
        super(BindDomainConfig, self).__init__(service=service)
        self.service = service
        self.domain = domain

    def get_template_name(self):
        return self.service.name + '_domain'

    def get_etc_parts(self):
        return 'sites-enabled', self.domain.name + '.conf'

    def get_context(self):
        context = super(BindDomainConfig, self).get_context()
        context['domain'] = self.domain

        template_serial = serial.for_file(self.template.filename)
        config_serial = serial.for_file(path.env_config())
        context['serial'] = max(self.domain.account.serial, template_serial, config_serial)

        return context

    def enabled(self):
        return self.domain.generate and self.domain.account.enabled

configs = {
    'a': ApacheServiceConfig,
    'n': NginxServiceConfig,
    'u': UwsgiServiceConfig,
    'b': BindZoneConfig,
}


def init_services(server, config):
    """Initialize services from config."""
    result = {}
    for key, value in config.iteritems():
        result[key] = configs[key](server=server, **value)
    return result
