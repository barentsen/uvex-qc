OUTPUT="tmp/limiting-mags.csv"
echo "run,lm" > $OUTPUT
cat tmp/concatenated-summary-list.txt | gawk 'match($0, "^(r[^_]+).*\\s(\\S+)$", a) {print a[1] "," a[2]}' | sort >> $OUTPUT
