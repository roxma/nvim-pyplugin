
let s:dir = expand('<sfile>:p:h')

let s:channel = -1

func! pyplugin#start()
	let l:python3 = get(g:,'python3_host_prog','')
	if l:python3 == ''
		let l:python3 = 'python3'
	endif
	call jobstart(l:python3 . ' ' . s:dir . '/../pysrc/run.py ' . v:servername, {'on_exit': function('s:on_exit')})
endfunc

func! s:on_exit()
	echom 'pyplugin exit'
	augroup pyplugin
		autocmd! pyplugin
	augroup end
endfunc

func! pyplugin#rpc_started(channel_id)

	let s:channel = a:channel_id

	augroup pyplugin

		autocmd!

		" TODO: 
		" event bindings
		autocmd BufLeave     * call s:on_event({'event': 'BufLeave'     , 'bufnr': bufnr('%')})
		autocmd BufEnter     * call s:on_event({'event': 'BufEnter'     , 'bufnr': bufnr('%')})
		autocmd BufRead      * call s:on_event({'event': 'BufRead'      , 'bufnr': bufnr('%')})
		autocmd BufNewFile   * call s:on_event({'event': 'BufNewFile'   , 'bufnr': bufnr('%')})
		" autocmd FileType     * call s:on_event({'event': 'FileType'     , 'bufnr': bufnr('%') , 'filetype': expand('<amatch>') })
		" autocmd TextChangedI * call s:on_event({'event': 'TextChangedI' , 'bufnr': bufnr('%') , 'filetype':&filetype , 'changedtick':b:changedtick})
		" ...

	augroup end

endfunc

func! s:on_event(event)
	try
		call rpcnotify(s:channel , 'event', a:event)
	catch
		" rpc send failed, the process may have exited and on_exit has not been called yet
		return
	endtry
endfunc

