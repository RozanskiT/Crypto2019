#/bin/bash

script_name="raport_dieharder.sh"

for f in *; do
  if [ "$f" != "${script_name}" ]; then
    a="_raport"
    echo "dieharder -a -f $f > $f$a"
    dieharder -a -f $f > $f$"_raport"
  fi

  
done
