# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

if [ -d $HOME/panard-config ]; then
    source $HOME/panard-config/conf_env
fi

if [ -d $HOME/panard-config/bin ]; then
    export PATH="$PATH:$HOME/panard-config/bin"
fi

if [ -f $CONF_PATH/path_env ]; then
    source $CONF_PATH/path_env
fi

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# don't put duplicate lines in the history. See bash(1) for more options
# ... or force ignoredups and ignorespace
HISTCONTROL=ignoredups:ignorespace

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=4000
HISTFILESIZE=8000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

    #PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[01;31m\]@\[\033[01;36m\]10.9.8.9\[\033[01;34m\]:\[\033[01;32m\]\w\[\033[01;31m\]>>>\[\033[00m\] '
    PS1='\[\033[01;36m\]\h\[\033[01;34m\]:\[\033[01;32m\]\w\[\033[00m\]\n\[\033[01;31m\][\t]\[\033[01;32m\]\u\[\033[01;31m\]==>\[\033[00m\] '
    #PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[01;31m\]@\[\033[01;36m\]\h\[\033[01;34m\]:\[\033[01;32m\]\w\[\033[01;31m\]>>>\[\033[00m\] '
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# some more ls aliases
if [ -f $CONF_PATH/alias ]; then
    source $CONF_PATH/alias
fi


#function _update_ps1() {
   #export PS1="$(~/bin/powerline-bash.py $?)"
#}

#export PROMPT_COMMAND="_update_ps1"

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
#if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
#    . /etc/bash_completion
#fi

#ls colors from linux deepin
if [[ ("$TERM" = *256color || "$TERM" = screen* || "$TERM" = xterm* ) && -f $CONF_PATH/lscolor-256color ]]; then
    eval $(dircolors -b $CONF_PATH/lscolor-256color)
else
    eval $(dircolors)
fi

#ignore case while auto completion
set completion-ignore-case on

if [ -f $HOME/.alias ]; then
    source $HOME/.alias
fi


if [ -f $HOME/.env ]; then
    source $HOME/.env
fi


bind '"\e[A": history-search-backward'
bind '"\e[B": history-search-forward'


function xgrep() {
    grep --color=auto -nHri "$@" ./*
}

function xread() {
    read -p "Press enter to continue"
}




# BEGIN functions from android build system
function getandroidtop
{
    local TOPFILE=build/core/envsetup.mk
    if [ -n "$TOP" -a -f "$TOP/$TOPFILE" ] ; then
        # The following circumlocution ensures we remove symlinks from TOP.
        (cd $TOP; PWD= /bin/pwd)
    else
        if [ -f $TOPFILE ] ; then
            # The following circumlocution (repeated below as well) ensures
            # that we record the true directory name and not one that is
            # faked up with symlink names.
            PWD= /bin/pwd
        else
            local HERE=$PWD
            local T=
            while [ \( ! \( -f $TOPFILE \) \) -a \( $PWD != "/" \) ]; do
                \cd ..
                T=`PWD= /bin/pwd -P`
            done
            \cd $HERE
            if [ -f "$T/$TOPFILE" ]; then
                echo $T
            fi
        fi
    fi
}

function gdir () {
    if [[ -z "$1" ]]; then
        echo "Usage: gdir <regex>"
        return
    fi
    local T=$(getandroidtop)
    local FILELIST
    if [ ! "$OUT_DIR" = "" ]; then
        mkdir -p $OUT_DIR
        FILELIST=$OUT_DIR/filelist
    else
        FILELIST=$T/filelist
    fi
    if [[ ! -f $FILELIST ]]; then
        echo "No index file, please create index file first"
        #(\cd $T; find . -wholename ./out -prune -o -wholename ./.repo -prune -o -type f > $FILELIST)
        #echo " Done"
        #echo ""
    fi
    local lines
    lines=($(\grep -i "$1" $FILELIST | sed -e 's/\/[^/]*$//' | sort | uniq))
    if [[ ${#lines[@]} = 0 ]]; then
        echo "Not found"
        return
    fi
    local pathname
    local choice
    if [[ ${#lines[@]} > 1 ]]; then
        while [[ -z "$pathname" ]]; do
            local index=1
            local line
            for line in ${lines[@]}; do
                printf "%6s %s\n" "[$index]" $line
                index=$(($index + 1))
            done
            echo
            echo -n "Select one: "
            unset choice
            read choice
            if [[ $choice -gt ${#lines[@]} || $choice -lt 1 ]]; then
                echo "Invalid choice"
                continue
            fi
            pathname=${lines[$(($choice-1))]}
        done
    else
        pathname=${lines[0]}
    fi
    \cd $T/$pathname
}
# BEGIN functions from android build system


bind 'set show-all-if-ambiguous on'
bind 'TAB:menu-complete'


