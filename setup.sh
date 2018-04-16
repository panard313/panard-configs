echo setup persional configs.....
set + x


set_config()
{
    filename=`echo $1 |awk -F '/' '{print $NF}'`
    echo link $filename
    cd ~/
    if [ -f ~/.$filename ];then
        mv ~/.$filename ~/.$filename.bak
    fi
    ln -s panard-configs/$1 ~/.$filename
}

cd ~/
ln -s panard-configs panard-config
set_config bashrc
set_config tmux.conf
set_config zshrc
set_config vim/vimrc.before.local
set_config vim/vimrc.bundles.local
set_config vim/vimrc.local
set_config git/gitconfig

echo done...
