# run in the form: python3 label-scraping.py [company name with words separated by spaces(not case sensitive)] i.e. python3 label-scraping.py Cocoa puffs
rm -f labels.txt
python label-scraping.py $@ > labels.txt
