# crossplane-update

A helper script for updating the directive definitions in
crossplane.analyzer.DIRECTIVES.

## Installation

    make install

## Usage

This script downloads the latest nginx release tarball, unpacks it, and searches
the source code for each directive's definition bitmask. This is very convenient
for NGINX OSS directives, but not for NGINX+ directives.

### Updating NGINX OSS directives automatically

You should just be able to run the script and copy-paste the output into the
crossplane/analyzer.py file.

    crossplane-update


### Updating NGINX+ directives manually

The dict output from the script above should end with a bunch of empty lists
for directives that were not in the NGINX OSS source code. For each of these
directives you should do this process:

1. Find the directive in http://nginx.org/en/docs/dirindex.html and follow the
   link to its documentation.

2. Find the context bitmask(s). Use this table to determine which to use:

    | Context                    | Bitmask(s)                                                    |
    | -------------------------- | ------------------------------------------------------------- |
    | any                        | `NGINX_ANY_CONF`                                              |
    | main (/http/ in url)       | `NGX_HTTP_MAIN_CONF`                                          |
    | main (/mail/ in url)       | `NGX_MAIL_MAIN_CONF`                                          |
    | main (/stream/ in url)     | `NGX_STREAM_MAIN_CONF`                                        |
    | main                       | `NGX_MAIN_CONF`                                               |
    | server (/http/ in url)     | `NGX_HTTP_SRV_CONF`                                           |
    | server (/mail/ in url)     | `NGX_MAIL_SRV_CONF`                                           |
    | server (/stream/ in url)   | `NGX_STREAM_SRV_CONF`                                         |
    | server                     | `NGX_HTTP_SRV_CONF | NGX_MAIL_SRV_CONF | NGX_STREAM_SRV_CONF` |
    | upstream (/http/ in url)   | `NGX_HTTP_UPS_CONF`                                           |
    | upstream (/stream/ in url) | `NGX_STREAM_UPS_CONF`                                         |
    | upstream                   | `NGX_HTTP_UPS_CONF | NGX_STREAM_UPS_CONF`                     |
    | http                       | `NGX_HTTP_MAIN_CONF`                                          |
    | mail                       | `NGX_MAIL_MAIN_CONF`                                          |
    | stream                     | `NGX_STREAM_MAIN_CONF`                                        |
    | events                     | `NGX_EVENT_CONF`                                              |
    | location                   | `NGX_HTTP_LOC_CONF`                                           |
    | if                         | `NGX_HTTP_SIF_CONF | NGX_HTTP_LIF_CONF`                       |
    | if in server               | `NGX_HTTP_SIF_CONF`                                           |
    | if in location             | `NGX_HTTP_LIF_CONF`                                           |
    | limit_except               | `NGX_HTTP_LMT_CONF`                                           |

3. Find the syntax bitmask(s). If the answer here is ambiguous, then check to
   see if there's a similar directive and do it the same way. Usually it will be
   pretty straight-forward though. This table should be helpful for determining
   the appropriate bitmask(s):

    | Bitmask(s)          | Meaning                                               |
    | ------------------- | ----------------------------------------------------- |
    | `NGINX_CONF_NOARGS` | The directive takes no arguments.                     |
    | `NGX_CONF_TAKE1`    | The directive takes exactly 1 argument.               |
    | `NGX_CONF_TAKE2`    | The directive takes exactly 2 arguments.              |
    | `NGX_CONF_TAKE3`    | The directive takes exactly 3 arguments.              |
    | `NGX_CONF_TAKE4`    | The directive takes exactly 4 arguments.              |
    | `NGX_CONF_TAKE5`    | The directive takes exactly 5 arguments.              |
    | `NGX_CONF_TAKE6`    | The directive takes exactly 6 arguments.              |
    | `NGX_CONF_TAKE7`    | The directive takes exactly 7 arguments.              |
    | `NGX_CONF_TAKE12`   | The directive takes 1 or 2 arguments.                 |
    | `NGX_CONF_TAKE13`   | The directive takes 1 or 3 arguments.                 |
    | `NGX_CONF_TAKE23`   | The directive takes 2 or 3 arguments.                 |
    | `NGX_CONF_TAKE123`  | The directive takes between 1 and 3 arguments.        |
    | `NGX_CONF_TAKE1234` | The directive takes between 1 and 4 arguments.        |
    | `NGX_CONF_BLOCK`    | The directive is a block directive.                   |
    | `NGX_CONF_FLAG`     | The directive takes 1 argument that is "on" or "off". |
    | `NGX_CONF_ANY`      | The directive takes any amount of arguments.          |
    | `NGX_CONF_1MORE`    | The directive takes 1 or more arguments.              |
    | `NGX_CONF_2MORE`    | The directive takes 2 or more arguments.              |
