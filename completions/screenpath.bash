# bash completion for screenpath
# shellcheck shell=bash disable=SC2207

_screenpath() {
  local cur prev opts
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"
  opts="-d --dir -p --prefix --tmp -w --window -f --full -i --image \
        -Q --quote -u --url -l --link -n --no-clip --notify --setup \
        -v --version -h --help install-raycast"

  # Value-taking flags: complete a directory for --dir, leave --prefix free.
  case "$prev" in
    -d|--dir) COMPREPLY=( $(compgen -d -- "$cur") ); return ;;
    -p|--prefix) return ;;
  esac

  # `install-raycast <dir>` completes a directory.
  if [ "${COMP_WORDS[1]}" = "install-raycast" ] && [ "$COMP_CWORD" -ge 2 ]; then
    COMPREPLY=( $(compgen -d -- "$cur") )
    return
  fi

  COMPREPLY=( $(compgen -W "$opts" -- "$cur") )
}

complete -F _screenpath screenpath
