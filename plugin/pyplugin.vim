
if v:vim_did_enter
	call pyplugin#start()
else
	au VimEnter * call pyplugin#start()
endif

