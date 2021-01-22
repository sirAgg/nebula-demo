" compile and run commands
"set makeprg="ninja -C build \| ffnffp.exe"
nnoremap <f3> :wa<cr>:silent! cexpr system(".\\fips build")<cr>:cw<cr>
nnoremap <S-f3> :wa<cr>:!ninja -C build\ -t clean<cr>:silent! cexpr system(".\fips clean && .\fips build")<cr>:cw<cr>
nnoremap <f4> :call RunProgram(".\\fips run nebula-demo")<cr>

nnoremap <f8> :!explorer .<cr><cr>
nnoremap <f7> :!devenv .<cr><cr>

nnoremap <leader>m :call ToggleHeader()<cr>
nnoremap <leader>e :Files ..<cr>

au BufRead,BufNewFile * set nonumber
au BufRead,BufNewFile *.ogge set number

"let g:ctrlp_custom_ignore = {
"  \ 'dir':  '\v[\/]\.(git|hg|svn)|target|build|Build|bin|docs$',
"  \ 'file': '\v\.(exe|so|dll|ttf|png)$',
"  \ 'link': 'some_bad_symbolic_links',
"  \ }

function! s:insert_gates()
  let gatename = substitute(toupper(expand("%:t")), "\\.", "_", "g")
  execute "normal! i#ifndef " . gatename
  execute "normal! o#define " . gatename . " "
  execute "normal! Go#endif /* " . gatename . " */"
  normal! kk
endfunction
autocmd BufNewFile *.{h,hpp} call <SID>insert_gates()

function! s:insert_include()
  let gatename = expand("%:t:r") . ".h"
  if(filereadable(expand("%:h") . "\\" . gatename))
      execute "normal! i#include \"" . gatename . "\""
      normal! kk
  endif
endfunction
autocmd BufNewFile *.{c,cpp,cc} call <SID>insert_include()

command -nargs=1 SetExecutable call SetExe(<f-args>)

function SetExe(file)
    let command = 'nnoremap <f4> :call RunProgram("bin\\' . a:file . '.exe")<cr>'
    execute command
endfunction

function ToggleHeader()
    let type = expand("%:e")
    if type=="h"
        if filereadable(expand("%:r") . ".cpp")
            :e %:r.cpp
        elseif filereadable(expand("%:r") . ".c")
            :e %:r.c
        else
            :e %:r.cc
        endif
    elseif type=="cc"
        :e %:r.h
    elseif type=="cpp"
        :e %:r.h
    elseif type=="c"
        :e %:r.h
    endif
endfunction


let g:buffnr = -1
function RunProgram(path_arg)
    if(g:buffnr < 0 || !bufexists(g:buffnr))
        execute '10sp'
        execute 'terminal ' . a:path_arg
        let g:buffnr = bufnr('%')
    else
        let winnr = bufwinnr(g:buffnr)
        if(winnr > 0)
            execute winnr 'wincmd w'
            execute 'terminal ' . a:path_arg
        else
            execute '10sp'
            execute 'buffer ' . g:buffnr
            execute 'terminal ' . a:path_arg
        endif

        execute 'bdelete! ' . g:buffnr
        let g:buffnr = bufnr('%')
    endif
    execute "normal! a"
endfunction


function FixFilePathInQF()
    let list = getqflist()
    for e in list
        let name = bufname(e.bufnr)[0:2] 
        if name ==? "..\\"
            echo e.bufnr ' ' bufname(e.bufnr)
        endif
    endfor
endfunction



