This is a bot written in python that runs in whatsapp and is purely an extension of [yowsup](https://github.com/tgalal/yowsup).

##Installation##
The installation process is quite simple

###One Time steps####

    git clone https://github.com/asdofindia/python-whatsapp-bot.git
    cd python-whatsapp-bot
    git submodule init
    git submodule update

####Associating with account ####
Follow [https://github.com/tgalal/yowsup/wiki/yowsup-cli#registration](https://github.com/tgalal/yowsup/wiki/yowsup-cli#registration) and register a number. After registering you must have created a config file as mentioned [here](https://github.com/tgalal/yowsup/wiki/yowsup-cli#your-login-credentials) like [this](https://github.com/tgalal/yowsup/blob/master/src/config.example)
Place the config file in `configs` folder.

## Running the bot ##
    python bot.py -c configs/<yourconfig> -b -a -k
    
if -c is not specified, `configs/config` will be used


##About
Look at my [older implementation](https://github.com/asdofindia/pyWhatsapp) to know more about how that used to work.
