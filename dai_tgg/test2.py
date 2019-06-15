import re
rs = re.search('(?=09).*','093434343')
print (rs.group(0))
