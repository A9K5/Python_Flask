
# Python's bundled WSGI server
from wsgiref.simple_server import make_server

def application (environ, start_response):

    # Sorting and stringifying the environment key, value pairs
    response_body = [
        '%s: %s' % (key, value) for key, value in sorted(environ.items())
    ]
    response_body = '\n'.join(response_body)

    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)

    return [response_body]

# Instantiate the server
httpd = make_server (
    'localhost', # The host name
    8051, # A port number where to wait for the request
    application # The application object name, in this case a function
)

# Wait for a single request, serve it and quit
httpd.handle_request()


# The response is :
# Apple_PubSub_Socket_Render: /private/tmp/com.apple.launchd.Ibs55r9F0a/Render
# COLORTERM: truecolor
# CONTENT_LENGTH: 
# CONTENT_TYPE: text/plain
# GATEWAY_INTERFACE: CGI/1.1
# HOME: /Users/ankurkumar
# HTTP_ACCEPT: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
# HTTP_ACCEPT_ENCODING: gzip, deflate, br
# HTTP_ACCEPT_LANGUAGE: en-GB,en-US;q=0.9,en;q=0.8
# HTTP_CACHE_CONTROL: max-age=0
# HTTP_CONNECTION: keep-alive
# HTTP_COOKIE: remember_token=1|fff4eca7680932ccdf019f265f5a7f1e686cedd6b8b4245d0790d2d26bc73008435d864d118f59f87bcdce470d632795ef4724fd42042cf09715700f61017732; session=.eJwljksKQjEMAO_StWCTNGn7LiNtk_BcqPA-IIh3t-BuZjPMJ9x8s30Ny7Gddgm3u4YlsLvAgCapoHeuHo2pQ8WYhTkydqRCSVWw5ESSi-oQb40xMSqWYljAtQ8DTF0opyiDvGKrkYVYMRMKeoxcGZx9dqt0zsBgRGGOnLtt_xuY-rT3MfG6vh4Wvj_hbTFf.X1E-kg.xHMcpmtCx5wKUl3whNwx56SCTg4; username-localhost-8888="2|1:0|10:1599404663|23:username-localhost-8888|44:OGU5NjgwMWFmNGZkNDkzNGE0MDgzOTdlZTY2NmY0NDg=|e774508b664591920127aeb7644f305212aac6a8b82afbdc99aa181b2681d3a4"; _xsrf=2|21b5152d|9e37b98a5af13f6f825e10da29a66d4a|1599404663
# HTTP_HOST: localhost:8051
# HTTP_REFERER: http://wsgi.tutorial.codepoint.net/environment-dictionary
# HTTP_SEC_FETCH_DEST: document
# HTTP_SEC_FETCH_MODE: navigate
# HTTP_SEC_FETCH_SITE: none
# HTTP_SEC_FETCH_USER: ?1
# HTTP_UPGRADE_INSECURE_REQUESTS: 1
# HTTP_USER_AGENT: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36
# LANG: en_GB.UTF-8
# LOGNAME: ankurkumar
# OLDPWD: /Users/ankurkumar/Documents/Git/Python_Flask
# PATH: /Library/Frameworks/Python.framework/Versions/3.8/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Library/Frameworks/Python.framework/Versions/3.8/bin
# PATH_INFO: /
# PS1: \h:\W \u\$ 
# PWD: /Users/ankurkumar/Documents/Git/Python_Flask/08_09_20
# QUERY_STRING: 
# REMOTE_ADDR: 127.0.0.1
# REMOTE_HOST: 1.0.0.127.in-addr.arpa
# REQUEST_METHOD: GET
# SCRIPT_NAME: 
# SERVER_NAME: 1.0.0.127.in-addr.arpa
# SERVER_PORT: 8051
# SERVER_PROTOCOL: HTTP/1.1
# SERVER_SOFTWARE: WSGIServer/0.1 Python/2.7.16
# SHELL: /bin/bash
# SHLVL: 2
# SSH_AUTH_SOCK: /private/tmp/com.apple.launchd.dZD5tz8mXd/Listeners
# TERM: xterm-256color
# TERM_PROGRAM: vscode
# TERM_PROGRAM_VERSION: 1.40.1
# TMPDIR: /var/folders/bp/6x6k_45j74s69gyskx9r5bxw0000gn/T/
# USER: ankurkumar
# VERSIONER_PYTHON_PREFER_32_BIT: no
# VERSIONER_PYTHON_VERSION: 2.7
# XPC_FLAGS: 0x0
# XPC_SERVICE_NAME: 0
# _: /usr/bin/python
# __CF_USER_TEXT_ENCODING: 0x1F5:0x0:0x0
# wsgi.errors: <open file '<stderr>', mode 'w' at 0x1016221e0>
# wsgi.file_wrapper: wsgiref.util.FileWrapper
# wsgi.input: <socket._fileobject object at 0x10175d250>
# wsgi.multiprocess: False
# wsgi.multithread: True
# wsgi.run_once: False
# wsgi.url_scheme: http
# wsgi.version: (1, 0)