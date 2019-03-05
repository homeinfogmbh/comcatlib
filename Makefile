FILE_LIST = ./.installed_files.txt

.PHONY: pull push clean install uninstall

default: | pull clean install

install: install-pyton install_locales

install-pyton:
	@ ./setup.py install --record $(FILE_LIST)

install-locales:
	@ mkdir -p /usr/local/etc/comcat.d/locales/de_DE
	@ msgfmt -v files/locales/de_DE/comcatlib.po -o /usr/local/etc/comcat.d/locales/de_DE/comcatlib.mo

uninstall:
	@ while read FILE; do echo "Removing: $$FILE"; rm "$$FILE"; done < $(FILE_LIST)

clean:
	@ rm -Rf ./build

pull:
	@ git pull

push:
	@ git push
