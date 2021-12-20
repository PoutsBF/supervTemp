#! /usr/bin/env python

from fbapp import app
import logging as lg

lg.getLogger().setLevel(lg.INFO)

if __name__ == "__main__":
    app.run(debug=True)