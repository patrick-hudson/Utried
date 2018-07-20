###
# Copyright (c) 2016, cottongin
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import base64
import requests
import json
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Utried')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class Utried(callbacks.Plugin):
    """Adds irc nick to gold star you tried image and provides link to channel"""
    threaded = True

    def __init__(self, irc):
        self.__parent = super(Utried, self)
        self.__parent.__init__(irc)

        try:
            self.imgurClientId = self.registryValue('ImgurClientId')
            self.imgurAPIKey = self.registryValue('ImgurAPIKey')
        except:
            #irc.error('Utried [ERR] check imgur registry values.', Raise=True)
            self.log.error('Utried :: utried :: Imgur value(s) not set. '
                '(config.supybot.plugins.Utried.Imgur*)')

        self.imgurURL = self.registryValue('ImgurURL')

        try:
            self.utried_image = self.registryValue('utriedImage')
            self.utried_font = self.registryValue('utriedFont')
        except:
            #irc.error('Utried [ERR] check utried registry values.', Raise=True)
            self.log.error('Utried :: utried :: utried value(s) not set. '
                '(config.supybot.plugins.Utried.utried*)')

        self.utried_default = self.registryValue('utriedDefault')

    def utried(self, irc, msg, args, optnick):
        """[<nick>]
        Returns a gold star with optional nick
        """
        
        if optnick:
            optnick = optnick.strip()
            img = Image.open(self.utried_image)
            W, H = img.size
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(self.utried_font, 58)
            w, h = draw.textsize(optnick, font)
            draw.text(((W-w)/2,275),optnick,(0,0,0),font=font)
            img.save('out.jpg')
            f = open('out.jpg', 'rb')
            bin = f.read()
            f.close()
            b64image = base64.b64encode(bin)
            headers = {"Authorization": "Client-ID %s" % (self.imgurClientId)}
            payload = {'key': self.imgurAPIKey, 'image': b64image, 'title': 'utried',}
            r = requests.post(self.imgurURL, headers=headers, data=payload)
            j = json.loads(r.text)
            irc.reply(j['data']['link'])
        else:
            irc.reply(self.utried_default)
    
    utried = wrap(utried, [optional('nick')])

Class = Utried


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
