#!/bin/bash

#########################################################################
#
#   2009-04-23  File created
#
#########################################################################

PROG=$(basename "$0")
VERSION="0.4"

# change default parameters here
SING_ARG='{}'
MULT_ARGS='{}+'
DEFAULT_CMD='echo'

printUsage() {
	echo "Usage: $PROG [--help] TEST_SPEC [FILE]... [--] [COMMAND [ARG]...]"
}

helpText() {
	local s='                       '
cat << -EOF-
$PROG $VERSION

Test files on the command line and do something

$(printUsage)

TEST_SPEC is a character string of unary file tests (e.g. 'fx' for "-f FILE -a
-x FILE"), which can be combined with the logical operators 'a' for "and"
(the default), 'o' for "or", and '!' or 'n' for "not". Parentheses can be used
for grouping. For example, use 'f\(nronw\)' for "-f FILE -a ( ! -r FILE -o
! -w FILE )". If FILE is not specified, a glob (*) in the current directory is
performed. If COMMAND is not specified, it defaults to \`$DEFAULT_CMD'. Any '$SING_ARG'
present in COMMAND or an ARG is replaced by FILE and executed for each FILE
that matches. However, if '$MULT_ARGS' is one of the ARGs, the command is only
invoked once, with the token replaced by a list of all the FILEs that matched.
If neither is in COMMAND or one of its ARGs, each FILE is appended to COMMAND,
which is then executed. If no file passes TEST_SPEC, do nothing and return 1.

Examples:
 $PROG x foo*                 \`$DEFAULT_CMD' all executables starting with "foo"
 $PROG d bar/* mv $SING_ARG $SING_ARG.bak${s:$((16+${#SING_ARG}*2))}append ".bak" to all directories in "bar"
 $PROG f [--] rm $MULT_ARGS baz${s:$((14+${#MULT_ARGS}))}remove all files plus "baz" in the current directory
 $PROG fx $SING_ARG${s:$((3+${#SING_ARG}))}run each executable file in the current directory

NOTE that '--' is needed as a separator if COMMAND exists in the current
directory, if COMMAND is an absolute path, or if one or more FILEs is possibly
nonexistent.

-EOF-
}

if [ "$1" = "--help" -o "$1" = "-h" ]; then
	helpText && exit
elif [ "$1" = "-?" ]; then
	printUsage && exit
fi

shopt -s dotglob
IFS=$'\n'

condition=()
cond_places=()
sep=
bang=

for (( i = 0; i < ${#1}; i++ )); do
	c="${1:$i:1}"
	if [ "$c" = "o" ]; then
		sep="-o"
	elif [ "$c" = "a" ]; then
		sep="-a"
	elif [[ "$c" == "!" || "$c" == "n" ]]; then
		bang="!"
	elif [[ "$c" == "(" ]]; then
		condition+=($sep $bang "$c")
		sep= && bang=
	elif [[ "$c" == ")" ]]; then
		condition+=("$c")
		sep="-a" && bang=
	elif [[ "$c" == [efdhLrwxsbcgGkOpSu] ]]; then
		condition+=($sep $bang -$c "")
		cond_places+=($(( ${#condition[@]} - 1 )))
		sep="-a" && bang=
	else
		printUsage >&2
		echo >&2
		echo >&2 "$PROG: bad unary file test: $c"
		exit 2
	fi
done
shift

if [ ! "$condition" ]; then
	printUsage >&2
	exit 2
fi

expect=

for arg in "$@"; do
	if [ "$arg" = "--" ]; then
		expect=1
		break
	fi
done

files=()

for arg in "$@"; do
	if [ "$arg" = "--" ]; then
		shift && break
	elif [ -e "$arg" ]; then
		files+=("$arg")
	elif [ "$expect" ]; then
		files+=("$arg")
	elif [[ "$arg" =~ (^|[^\\])(\\\\)*([*?]|\[[^!^/][^/]*\]|\[[!^][^/]+\]|[*?+@!]\([^/]+\)) ]]; then
		files+=("$arg")
	else
		break
	fi
done
shift ${#files[@]}

if [ ! "$files" ]; then
	files=(*)
	[ ! -e "$files" ] && exit 1
fi

ESC=\\

cmd=()
cmd_post=()
file_places=()
m_args=

for arg in "$@"; do
	if [ "$m_args" ]; then
		cmd_post+=("$arg")
	else
		if [ "$arg" = "$MULT_ARGS" ]; then
			m_args=1
			continue
		elif [[ "$arg" =~ ${ESC}$SING_ARG ]]; then
			file_places+=(${#cmd[@]})
		fi
		cmd+=("$arg")
	fi
done

[ ${#cmd[@]} -eq 0 ] && cmd="$DEFAULT_CMD"

if [ "$m_args" ]; then

	list=()

	for file in "${files[@]}"; do
		for i in "${cond_places[@]}"; do
			condition[$i]="$file"
		done
		if [ "${condition[@]}" ]; then
			list+=("$file")
		fi
	done

	if [ ${#list[@]} -gt 0 ]; then
		"${cmd[@]}" "${list[@]}" "${cmd_post[@]}"
		exit
	else
		exit 1
	fi

fi

exitcode=0

max() {
	if [ $1 -gt $2 ]; then
		echo $1
	else
		echo $2
	fi
}

match=

for file in "${files[@]}"; do

	for i in "${cond_places[@]}"; do
		condition[$i]="$file"
	done

	if [ "${condition[@]}" ]; then
		match=1

		if [ "$file_places" ]; then
			run=("${cmd[@]}")
			for i in "${file_places[@]}"; do
				run[$i]="${cmd[$i]//$SING_ARG/$file}"
			done
			"${run[@]}"
		else
			"${cmd[@]}" "$file"
		fi

		code=$?
		if [ $code -eq 127 ]; then
			exit 127
		elif [ $code -ne 0 ]; then
			exitcode=$(max $code $exitcode)
		fi
	fi

done

if [ "$match" ]; then
	exit $exitcode
else
	exit 1
fi

# vim:set ts=4 sw=4 noet:
