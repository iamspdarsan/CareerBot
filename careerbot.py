import json
import modules as core

qlfile='userdata\\filteredqlink'
qlink=json.load(open(qlfile,'r'))
core.applyjobs(qlink)