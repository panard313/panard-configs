if [ -d $HOME/panard-configs ]; then 
   source $HOME/panard-configs/conf_env
   CONF_PATH=$HOME/panard-configs
fi

if [ -f $CONF_PATH/path_env  ]; then
    source $CONF_PATH/path_env
fi


# Path to your oh-my-zsh installation.
ZSH=$CONF_PATH/oh-my-zsh/

# Set name of the theme to load.
# Look in ~/.oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
#ZSH_THEME="agnoster-cx"
ZSH_THEME="candy-cx"

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(autosuggestions syntax-highlighting)

source $ZSH/oh-my-zsh.sh
[[ -s /home/chenxiong/.autojump/etc/profile.d/autojump.sh ]] && source /home/chenxiong/.autojump/etc/profile.d/autojump.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/dsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

#some more ls aliases
if [ -f $CONF_PATH/alias ]; then
     source $CONF_PATH/alias
fi

if [ -f $CONF_PATH/z.sh ]; then
   source $CONF_PATH/z.sh
fi

case `uname` in
  Linux)
    # commands for Linux go here
	#ls colors from linux deepin
	if [[ ("$TERM" = *256color || "$TERM" = screen* || "$TERM" = xterm* ) && -f $CONF_PATH/lscolor-256color ]]; then
	    eval $(dircolors -b $CONF_PATH/lscolor-256color)
	else
	    eval $(dircolors)
	fi
  ;;
  Darwin)
    # commands for OS X go here
	#PATH for anaconda2

	export PATH=$PATH:/Volumes/CS-Data/Anaconda2/anaconda2/bin

	export PATH="/usr/local/opt/grep/libexec/gnubin:$PATH"

	# HomeBrew
	export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles
	export PATH="/usr/local/bin:$PATH"
	export PATH="/usr/local/sbin:$PATH"
	# HomeBrew END

	export LC_ALL=C
	export LC_ALL=en_US.UTF-8
	export LANG=en_US.UTF-8
  ;;
  FreeBSD)
    # commands for FreeBSD go here
  ;;
esac

PATH=$PATH:~/panard-configs/bin

PATH=/data/nishome/tdsw1/xiong.chen/Integrity/ILMClient12/bin:$PATH

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/data/nishome/tdsw1/xiong.chen/anaconda2/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/data/nishome/tdsw1/xiong.chen/anaconda2/etc/profile.d/conda.sh" ]; then
        . "/data/nishome/tdsw1/xiong.chen/anaconda2/etc/profile.d/conda.sh"
    else
        export PATH="/data/nishome/tdsw1/xiong.chen/anaconda2/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
