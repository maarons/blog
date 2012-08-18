.PHONY: all prepare server clean

all: prepare
	pelican -s pelican_conf.py

prepare: theme/static/css/main.css theme/static/css/html5shiv.js

theme/static/css/main.css: theme/static/css/_pygments.scss theme/static/css/main.scss theme/static/css/_common.scss
	sass theme/static/css/main.scss:theme/static/css/main.css

theme/static/css/_pygments.scss:
	pygmentize -S default -f html -a .codehilite > theme/static/css/_pygments.scss

theme/static/css/html5shiv.js:
	wget --tries=5 "https://raw.github.com/aFarkas/html5shiv/master/dist/html5shiv.js" -O theme/static/css/html5shiv.js

server: prepare utils/nginx.conf
	pelican -s pelican_conf_dev.py
	nginx -c "`pwd`/utils/nginx.conf"

utils/nginx.conf: utils/nginx.conf.template
	sed -e "s:ROOT:`pwd`/output:" utils/nginx.conf.template > utils/nginx.conf

clean:
	-rm -f theme/static/css/_pygments.scss
	-rm -f theme/static/css/main.css
	-rm -rf .sass-cache/
	-rm -f theme/static/css/html5shiv.js
	-rm -rf output/
	-rm -f utils/nginx.conf
	-rm -f *.py[co]
