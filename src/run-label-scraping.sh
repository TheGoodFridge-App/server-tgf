# run in the form: python3 label-scraping.py [company name with words separated by spaces(not case sensitive)] i.e. python3 label-scraping.py Cocoa puffs
rm -f src/labels.txt
python src/label-scraping.py $@ > src/labels.txt
