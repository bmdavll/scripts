#!/usr/bin/perl
# Finding special characters in Google result URLs.

# Your Google API developer's key.
my $google_key='insert key here';

# Number of times to loop, retrieving 10 results at a time.
my $loops = 10;

# Location of the GoogleSearch WSDL file.
my $google_wdsl = "./GoogleSearch.wsdl";

use strict;

use CGI qw/:standard/;
use SOAP::Lite;

print
  header( ),
  start_html("Aunt Tilde"),
  h1("Aunt Tilde"),
  start_form(-method=>'GET'),
  'Query: ', textfield(-name=>'query'),
  br( ),
  'Characters to find: ',
  checkbox_group(
    -name=>'characters',
    -values=>[qw/ ~ @ ? ! /],
    -defaults=>[qw/ ~ /]
  ),
  br( ),
  submit(-name=>'submit', -value=>'Search'),
  end_form( ), p( );

if (param('query')) {

  # Create a regular expression to match preferred special characters.
  my $special_regex = '[\\' . join('\\', param('characters')) . ']';

  my $google_search  = SOAP::Lite->service("file:$google_wdsl");

  for (my $offset = 0; $offset <= $loops*10; $offset += 10) {
    my $results = $google_search ->
      doGoogleSearch(
        $google_key, param('query'), $offset, 10, "false", "",  "false",
        "", "latin1", "latin1"
      );

    last unless @{$results->{resultElements}};

    foreach my $result (@{$results->{'resultElements'}}) {

      # Output only matched URLs, highlighting special characters in red
      my $url = $result->{URL};
      $url  =~ s!($special_regex)!<font color="red">$1</font>!g and
        print
          p(
            b(a({href=>$result->{URL}},$result->{title}||'no title')), br( ),
            $url, br( ),
            i($result->{snippet}||'no snippet')
          );
    }
  }

  print end_html;
}
