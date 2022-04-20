#!/bin/bash
function to_absolute() {
    if [ "${1:0:1}" = "/" ]; then
        echo $1
    else
        echo $(pwd)/$1
    fi
}

function remote_transfer() {
    rsync -razP --exclude=build $1/ $2
}

function remote_compile() {
    ssh $1 "cd $2/build; cmake ..; make"
}

function compile() {
    cd $1/build
    cmake ..
    make
}

function main() {
    if [[ "$1" == "push" ]]; then
        remote_transfer $3 $2:$4
        remote_compile $2 $4 
    elif [[ "$1" == "pull" ]]; then
        remote_transfer $2:$3 $4
        compile $3
    fi
}

to_absolute $3
if [[ $# == 4 ]]; then
    apath1=$(to_absolute $3)
    apath2=$(to_absolute $4)
    main $1 $2 $apath1 $apath2
else
    apath=$(to_absolute $3)
    main $1 $2 $apath $apath
fi