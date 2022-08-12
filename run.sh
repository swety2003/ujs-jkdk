!#/bin/bash
docker run -e "ACCESS_KEY=admin" -v `pwd`/db:/code/db -d -p 8080:8000 ujsjkdk