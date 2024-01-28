# coding:utf-8
from tornado.web import RequestHandler
from traceback import format_exc
from app_base.app_redis import get_hash_map_cache, refresh_redis_cache
from app_base.app_log import warn
from app_base.utils import get_string, get_remote_ip, sequence_to_string
from constants.def_error_code import ERR_DEFAULT, ERR_ACCESS_DENIED
import re
from app_base.utils.pxfilter import filter_xss


class BaseHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request)
        self._http404_message = 'HTTPError: HTTP 404: Not Found'
        self._http500_message = 'HTTPError: HTTP 500: Internal Server Error'
        self._command_func_dict = kwargs.get('command_dict', {})

    def get(self, *args, **kwargs):
        self.post(*args, **kwargs)

    def post(self, *args, **kwargs):
        try:
            result = self.do_command(*args, **kwargs)
        except Exception, e:
            warn(ERR_DEFAULT, 'command exception', self.request.path,
                 self.request.arguments, '\n'.join([str(e), format_exc()]))
            result = self._http500_message
        finally:
            self.write(sequence_to_string(result))

    def do_command(self, *args, **kwargs):
        command = get_string(args[0])
        func = self._command_func_dict.get(command)
        if func:
            command_info = self.get_command_info(command)
            return func(command_info)
        else:
            warn(ERR_ACCESS_DENIED, 'command invalid',
                 self.request.path, self.request.arguments)
            return self._http404_message

    def get_command_info(self, command):
        params = {}
        for key, arguments in self.request.arguments.iteritems():
            params[get_string(key)] = arguments[-1]
        ip = self.get_remote_ip()
        render = self.render
        device = self.request.headers.get('User-Agent', '')
        files = self.request.files.get("file")  # input标签的 name = file
        u_id = self.get_secure_cookie("u_id")
        user_name = self.get_secure_cookie("user_name")
        token = self.get_secure_cookie("token")
        return CommandInfo(ip=ip, command=command, render=render, device=device, params=params,
                           u_id=u_id, user_name=user_name, token=token, files=files)

    def get_remote_ip(self):
        return get_remote_ip(self)


class ErrorHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(ErrorHandler, self).__init__(application, request, **kwargs)

    def get(self, *args, **kwargs):
        self.write(self._http404_message)

    def post(self, *args, **kwargs):
        self.write(self._http404_message)


class CommandInfo(object):
    def __init__(self, ip, command, render, device, params, u_id, user_name, token, files):
        super(CommandInfo, self).__init__()
        self.ip = ip
        self.command = command
        self.render = render
        self.params = params
        self.device = device
        self.u_id = u_id
        self.user_name = user_name
        self.token = token
        self.files = files


def get_post_command_dict(modules, pattern=r'^command_(\w+)$', ):
    command_dict = dict()

    def get_module_command(module):
        module_dict = module.__dict__
        for key in module_dict:
            r = re.search(pattern, key)
            if r:
                command_dict[r.group(1)] = module_dict[key]

    if isinstance(modules, list):
        for m in modules:
            get_module_command(m)
    else:
        get_module_command(modules)
    return command_dict


