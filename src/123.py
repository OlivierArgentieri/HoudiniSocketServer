import hou
import sys, os

path_to_append = ""
by_env = hou.getenv("HOUDINI_SCRIPT_PATH")
if by_env is not None:
    path_to_append = by_env.split("src")[0]

print(path_to_append)
sys.path.append(path_to_append) # todo

tmp_modules = sys.modules.copy()
for key, value in tmp_modules.iteritems():
    if key.startswith('src.'):
        sys.modules.pop(key, None)

if 'houdini' in sys.executable :
    from src.engines.handler.houdini.scripts import houdini_handler
else:
    from src.engines.handler.houdini.scripts import hython_handler