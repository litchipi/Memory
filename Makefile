OUT_NAME=archive.tar
ROOT   = $(HOME)/.backup
TMPDIR = '/tmp/bck_$(shell date +%d_%m_%y)'

ARCHIVE_CMD = tar -c -h -v --ignore-command-error -a -f

NO_OUT= 1>/dev/null 2>/dev/null

include gmsl

#assert_target_directory = $(call assert,$(wildcard $(dir $@)),Target directory $(dir $@) missing)

set = $(eval $1 := $2)

all: backup_compressed backup_encrypted backup_encrypted_compressed store_only
	@echo "Finished backuping parts"

reset:
	rm -rf $(ROOT)

prepare:
	@echo $(ARCHIVE_CMD)
	@rm -rf $(TMPDIR)
	@mkdir -p $(ROOT) $(TMPDIR)

final_archive:
	@echo "Final archive in $(ROOT)/$(OUT_NAME)"
	@cd $(TMPDIR) && tar cf $(ROOT)/$(OUT_NAME) ./*.tar* # $(NO_OUT)

finish: final_archive
	@rm -rf $(TMPDIR)

backup_encrypted: prepare
	$(call assert,$(ENC_PWD))
	$(call set,FILES,$(shell ./read_from_register.py $(ROOT) include e))
	$(call set,EXCLUDES_DIRS,$(foreach d, $(shell ./read_from_register.py $(ROOT) exclude dirs), --exclude='$d/**'))
	$(call set,EXCLUDES_FILES,$(foreach f, $(shell ./read_from_register.py $(ROOT) exclude files), --exclude='$f'))
	@echo "Backing up files to encrypt only"
	@mkdir -p $(TMPDIR)/enc/
	@for f in $(FILES); do ln -s "$$f" $(TMPDIR)/enc/ ; done
	@cd $(TMPDIR)/ && $(ARCHIVE_CMD) ./enc.tar $(EXCLUDES_DIRS) $(EXCLUDES_FILES) ./enc/
	@gpg -c --batch --passphrase $(ENC_PWD) $(TMPDIR)/enc.tar
	@rm $(TMPDIR)/enc.tar

backup_compressed: prepare
	$(call set,FILES,$(shell ./read_from_register.py $(ROOT) include c))
	$(call set,EXCLUDES_DIRS,$(foreach d, $(shell ./read_from_register.py $(ROOT) exclude dirs), --exclude='$d/**'))
	$(call set,EXCLUDES_FILES,$(foreach f, $(shell ./read_from_register.py $(ROOT) exclude files), --exclude='$f'))
	@echo "Backing up files to compress only"
	@mkdir -p $(TMPDIR)/cmp/
	@for f in $(FILES); do ln -s "$$f" $(TMPDIR)/cmp/ ; done
	@cd $(TMPDIR)/ && $(ARCHIVE_CMD) ./cmp.tar.xz $(EXCLUDES_FILES) $(EXCLUDES_DIRS) ./cmp/

backup_encrypted_compressed: prepare
	$(call assert,$(ENC_PWD))
	$(call set,FILES,$(shell ./read_from_register.py $(ROOT) include ce))
	$(call set,EXCLUDES_DIRS,$(foreach d, $(shell ./read_from_register.py $(ROOT) exclude dirs), --exclude='$d/**'))
	$(call set,EXCLUDES_FILES,$(foreach f, $(shell ./read_from_register.py $(ROOT) exclude files), --exclude='$f'))
	@echo "Backing up files to encrypt and compress"
	@mkdir -p $(TMPDIR)/enc_cmp/ 
	@for f in $(FILES); do ln -s "$$f" $(TMPDIR)/enc_cmp/ ; done
	@cd $(TMPDIR)/ && $(ARCHIVE_CMD) ./enc_cmp.tar.xz $(EXCLUDES_DIRS) $(EXCLUDES_FILES) ./enc_cmp/
	@gpg -c --batch --passphrase $(ENC_PWD) $(TMPDIR)/enc_cmp.tar.xz
	@rm $(TMPDIR)/enc_cmp.tar.xz

store_only: prepare
	$(call set,FILES,$(shell ./read_from_register.py $(ROOT) include s))
	$(call set,EXCLUDES_DIRS,$(foreach d, $(shell ./read_from_register.py $(ROOT) exclude dirs), --exclude='$d/**'))
	$(call set,EXCLUDES_FILES,$(foreach f, $(shell ./read_from_register.py $(ROOT) exclude files), --exclude='$f'))
	@echo "Backing up files to store only"
	@mkdir -p $(TMPDIR)/store/
	@for f in $(FILES); do ln -s "$$f" $(TMPDIR)/store/ ; done
	@cd $(TMPDIR)/ && $(ARCHIVE_CMD) ./store.tar $(EXCLUDES_DIRS) $(EXCLUDES_FILES) ./store/
