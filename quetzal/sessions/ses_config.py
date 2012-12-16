from quetzal import conf
import web

quetzal_config = conf.QuetzalConfig.load()


web.config.session_parameters['cookie_name'] = quetzal_config['cookie_name']
web.config.session_parameters['cookie_domain'] = quetzal_config['cookie_domain'] if quetzal_config['cookie_domain'] != "None" else None
web.config.session_parameters['timeout'] = int(quetzal_config['cookie_timeout'])
web.config.session_parameters['ignore_expiry'] = True
web.config.session_parameters['ignore_change_ip'] = True
web.config.session_parameters['secret_key'] = quetzal_config['cookie_secret_key']