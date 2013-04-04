lesscw
======

In short: `lesscw less/` will scan recursively `less` folder for `*.less` files and compile them into `.css`. It will rescan all folders within `less/` every 5 seconds (in `lesscw`: `FOLDER_SCAN_INTERVAL`).

* src: `lesscw.co` written in [coco language](https://github.com/satyr/coco/)
* bin: `lesscw`

## Installation

* get [node](nodejs.org/)
* get [npm](https://npmjs.org/)
* `npm install -g lesscw`
* or `git clone https://github.com/jan-swiecki/lesscw/ && cd lesscw && npm link`

have fun