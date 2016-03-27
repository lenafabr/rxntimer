opendir(DIR,".");
@jpgs = grep(/jpg$/,readdir(DIR));

foreach $f (@jpgs) {
    $f =~ m/(.*)\.jpg/;
    $root = $1;
# get the image information for this file
    $info = `identify $f`;
    print("$info\n");
    $info =~ m/ (\d+)x(\d+) /;
 # ratios of the width and height to what we want them to be
    $xrat = 190/$1*100;
    $yrat = 150/$2*100;
# resize dimensions appropriately
    if ($xrat < $yrat && $xrat < 100) {
#	print("convert -resize $xrat% $f $root.gif\n");
	`convert -resize $xrat% $f $root.gif`;
    } elsif ($yrat<$xrat && $yrat < 100) {
	`convert -resize $yrat% $f $root.gif`;
    } else {
	`convert $f $root.gif`;
    }
#    print("$xrat $yrat $m\n");
}

