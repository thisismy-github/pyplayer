'''
>>> UNFINISHED PROJECT <<<
This is an unfinished build of an unreleased project. It is very messy.
Soon(ish), this will be released on Github separately and eventually
released as a fully-fledged Python library.

This version is included purely for compatability purposes and will
inevitably be removed.
>>> UNFINISHED PROJECT <<<


TODO: .load() -> 5.6 sec/million
TODO: option to print out key/value pairs while loading
TODO: ability for user to auto-raise error on missing values
TODO: alternate class that always reads from the file?
TODO: alternate class that always WRITES to the file? (_ConfigParseBetter.__setattr__)
TODO: add more filler functions like remove_section
TODO: use getSection less?
TODO: work out sectionLock with dot notation + load() + etc.
TODO: low memory mode -> bettersectionproxy, attributes, etc.
TODO: errors with capitalization of options with dot notation?
TODO: base load()'s type on fallback or do try/excepts with typecasts?
TODO: function/attribute overhead stuff
TODO: typecasting multi-type lists (hello,500 -> ['hello', 500])
TODO: should "type(???) in __iterTypes" be a function with an isinstance for-loop?
TODO: change bsp to something readable
TODO: make sure you can do load('lastdir', '.') and cfg.lastdir = '.'
          - these MUST do the same thing when you load for the first time
TODO: loading something for the first time and then
      writing immediately does not update the value
TODO: make more parameters like fallback_align/__strip global AND line-by-line
          - will this significantly impact performance? probably not?
TODO: general performance. get rid of proxies? how efficient is saving/assigning?
TODO: finish lowMemoryMode or make subclass
TODO: type(x) in (types) VS. for type in types: isinstance(x)?
TODO: make ConfigparsebetterQt show args and kwargs correctly for __init__
TODO: .name vs .getName()
TODO: version without the lower() forcing (more efficient)
TODO: keep lower() but DON'T change case in file (very hard -> [OPTIONS] but .options works)
TODO: optional debug messages (search for #print)
TODO: WHOOPSIE --> cfg['general']['something'] = True --> LITERALLY CANNOT WORK
TODO: cfg['something'] = True --> also wouldn't work
TODO: I intentionally lowercased section names (in getSection and BSP.__setattr__)?
TODO: alternate-data-streams (ADS) -> https://www.daniweb.com/programming/tutorials/523626/creating-a-gui-wrapper-for-vlc-media-player-in-python-wxpython
TODO: add warning or fix for "stripvalues + delimiter ending in ' ' + ambiguous length" combo
TODO: way of performing action to each value, like "key" parameter in sort (like doing os.path.exists on every string in a list)

From main.pyw:
    - advanced radio button support (with min(max()))?
    - method for saving those things with the sliders like in BDL
    > POSSIBLE SOLUTIONS:
        > bite the bullet and get rid of OptionProxies? people will just have to do x = cfg.x and then cfg.x = x.
            - autosave involves just saving every attribute to its name with its own value
                - use generators to map expected typings to their actual types?
                    - recreate 2 generators everytime new load()'s are called
                        - one generator is the names of all values
                        - the other is the expected type for each corresponding value
            - add if-statement in __setattr__ that autosaves/writes edits
        > use __getattribute__ to directly intervene and get/set .value for items that are OptionProxies
            - this solves most problems, but introduces two new ones:
                - Proxies are no longer mutable in the reasonable sense (UNFIXABLE)
                - People who want to access the proxies themselves must use alternate methods
                    like .copy() or .proxy() or .get() or some other garbage
    - Deal with % signs. Somehow. https://stackoverflow.com/questions/46156125/how-to-use-signs-in-configparser-python
    - val_type to just type?
    - delimiter_type to list/tuple as default?
    - what is delimiter_type in save()?
    - better min_len and max_len -> use slicing to cut off unwanted parts with max_len?
    - change __types to __listtypes or something
    - align_with_fallback should also fill in default values based on index
    - improve the way empty values for delimited lists are handled. should the fallback just take over immediately?
        - is that how it already works?
'''

import os
import sys
import logging
import traceback
import configparser

logger = logging.getLogger('CPB')
#from inspect import getframeinfo, stack
#def info(*args, sep=' '):   # TODO remove this, temporary print() fixup
#    caller = getframeinfo(stack()[1][0])
#    log = sep.join(str(arg).lstrip() for arg in args)
#    logger.info(f'{caller.function:<11} [{caller.lineno:<3}] - {log}')
generator = type(_ for _ in ())

class LockedNameException(Exception):   # TODO finish this
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f'Option name "{self.name}" is not allowed ' \
               '(__parser, __section, __filepath, ' \
               '__sectionLock, __defaultExtension).'

class SetSectionToValueError(Exception):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f'Setting a section ("{self.name}") to a value is not allowed.'

class InvalidSectionError(Exception):
    def __init__(self, name, caller):
        self.name = name
        self.caller = caller
    def __str__(self):
        return f'{self.caller}: "{self.name}" is not a valid section.'




class OptionProxy:
    __slots__ = ('section', 'sectionDict', 'name')      # OptionProxies do not dynamically store values like BSP and CPB do

    def __init__(self, name, section_proxy, delimiter):
        self.section = section_proxy
        self.sectionDict = section_proxy.__dict__
        #self.sectionDict = self.section.__dict__
        self.name = name
        #self.delimiter = delimiter     # TODO use this? requires much more in-depth autosave

    def set(self, value):
        self.sectionDict[self.name] = value

    @property
    def value(self):
        #print('!!!!!!', self.name, self.section, self.sectionDict)
        return self.sectionDict[self.name]

    #def __getitem__(self, key): return self.value[key]
    #def __setitem__(self, key, val): self.value[key] = val
    #def __call__(self, *args, **kwargs): return self.value(*args, **kwargs)
    #def __contains__(self, val): return val in self.value
    #def __add__(self, other): return self.value + (other.value if isinstance(other, OptionProxy) else other)
    def __str__(self): return str(self.value)
    #def __repr__(self): return self.value      # causes crashes




class BetterSectionProxy:
    def __init__(self, parent, section):
        self.__parent = parent
        self.__section = self.__parent.getParser()[section]

    @property
    def name(self):
        return self.__section.name

    def getSettings(self):
        return dict(self.__parent.getParser().items(self.__section.name))

    def get(self, key):
        return self.__getattr__(key)

    def __getitem__(self, key):
        #try: return self.__parser[key]           # this is commented out in twitch CPB (GOOD.)
        #except: return None
        try: return self.__dict__[key]
        except:
            try: return self.__parent.getParser()[key]
            except: return None
        #try: return self.__getattr__(key)       # TODO twitch CPB
        #except:
        #    try: return self.__parent.getParser()[key]
        #    except: return None

    def __setitem__(self, key, value):
        #self.__parser[key] = value
        #print('\n\n\nSETTING ITEM', key, value, self.__section)
        self.__setattr__(key, value)               # TODO twitch CPB

    def __setattr__(self, name, value):
        if name[:19] != '_BetterSectionProxy':    # TODO (below) redundant?
            # TODO the following commented out lines were commented out in twitch CPB (all lines were present)
            #if type(value) in self.__parent._ConfigParseBetter__iterTypes:         # <-
            #    delimiter = self.__parent._ConfigParseBetter__defaultDelimiter     # <-
            #    self.__section[name] = delimiter.join(str(v) for v in value)       # <-
            #else:                                                                  # <-
            #    self.__section[name] = str(value)                                  # <-
            self.__parent.save(name, value, section=self.__section)
            self.__dict__[name.lower()] = value   # .lower()? and in __getattr__ too
            #self.__parent.__dict__[name.lower()] = value                           # <-
        else:
            self.__dict__[name.lower()] = value   # .lower()? and in __getattr__ too

    def __getattr__(self, name):    # handles dot notation when `name` does not exist
        #if not name.islower():
        #    try:
        #        name = name.lower()
        #        return self.__dict__[name]
        #    except: pass
        try: return self.__dict__[name.lower()]     # TODO this is very different from __getitem__
        except:
            try: return self.__parent.__dict__[name]
            except: return self.__section[name]

    def __contains__(self, other): return other in self.__dict__    # used near the end of _ConfigParseBetter.load()
    def __str__(self): return f'{self.name}: {self.getSettings()}'
    #def __repr__(self): return str(self.value)                     # causes crashes




class _ConfigParseBetter:
    def __init__(self, filepath=None, ConfigParserObject=None,
                 autoread=True, autosave=True, appdata=False,
                 section='general', stripValues=False,
                 autoUnpackLen1Lists=True, defaultExtension='.ini',
                 defaultDelimiter=',', sectionLock=False,
                 lowMemoryMode=False, autosaveCallback=True,
                 encoding=None, ConfigParserKwargs={}):
        ''' ConfigParserObject defaults to None because using objects as default
            values will always init them first, causing 2 ConfigParserObjects to
            be generated if the user passes in their own. '''
        self.__sectionLock = sectionLock
        self.__errorForMissingFallbacks = True  # TODO unused
        self.__stripValues = stripValues
        self.__autoUnpackLen1Lists = autoUnpackLen1Lists
        self.__defaultExtension = defaultExtension
        self.__defaultDelimiter = defaultDelimiter
        self.__lowMemoryMode = lowMemoryMode    # TODO unused
        self.__autosave = autosave
        self.__encoding = encoding

        self.__iterTypes = (generator, list, tuple, set)
        #self.__locked = tuple(self.__dict__.keys())     # TODO unused (use soon)
        #print(self.__locked, end='\n\n')

        if ConfigParserObject is None:
            self.__parser = configparser.ConfigParser(**ConfigParserKwargs)
        else:
            self.__parser = ConfigParserObject
        #self.__section = 'DEFAULT'  # TODO not needed anymore?
        self.__section = section    # default section if no section is loaded <- TODO twitch CPB

        self.__filepath = filepath
        if not filepath:
            if sys.argv[0]:
                self.__filepath = sys.argv[0].split('\\')[-1][:-3]
            else:
                if appdata:
                    import inspect
                    caller = inspect.stack()[-1][0].f_code.co_filename
                    base = os.path.splitext(os.path.basename(caller))[0]
                    self.__filepath = os.path.join(base, 'config')
                else:
                    self.__filepath = 'config'
        self.__filepath = self.createConfigPath(appdata=appdata)
        if autoread: self.read(self.__filepath, section, encoding=encoding)
        if autosave and autosaveCallback is not False:          # False -> no callback; True or None -> default callback
            import atexit
            if autosaveCallback is not True and autosaveCallback is not None:   # custom callback specified
                if type(autosaveCallback) in self.__iterTypes:      # callback is an array with arguments
                    kwargs_index = -1
                    for index, arg in enumerate(autosaveCallback):
                        if isinstance(arg, dict):
                            kwargs_index = index
                            break
                    if kwargs_index != -1:      # keyword arguments detected
                        if kwargs_index == 1:   # only keyword arguments detected
                            atexit.register(autosaveCallback[0],
                                            **autosaveCallback[1:])
                        else:                   # positional and keyword arguments detected
                            atexit.register(autosaveCallback[0],
                                            *autosaveCallback[1:kwargs_index],
                                            **autosaveCallback[kwargs_index:])
                    else:                       # no keyword arguments detected
                        atexit.register(autosaveCallback[0],
                                        *autosaveCallback[1:])
                else: atexit.register(autosaveCallback)         # callback includes no arguments
            else: atexit.register(self.write, appdata=appdata)  # use default callback (self.write)


    def createConfigPath(self, path=None, appdata=False):
        path = path if path else self.__filepath
        path = os.path.normpath(path)
        if appdata:
            appdatapath = os.path.expandvars('%LOCALAPPDATA%')
            if not path.lower().startswith(appdatapath.lower()):
                path = os.path.join(appdatapath, path)
        dirs, name = os.path.dirname(path), os.path.basename(path)
        if dirs and not os.path.exists(dirs):
            os.makedirs(dirs)
        if name[-4:] not in ('.ini', '.cfg'):
            name += self.__defaultExtension
        return os.path.join(dirs, name)


    def read(self, filepath=None, setSection=None, **kwargs):
        if setSection is not None: self.setSection(setSection)
        filepath = filepath or self.__filepath
        encoding = kwargs.get('encoding', self.__encoding)
        self.__parser.read(filepath, encoding=encoding)


    def write(self, filepath=None, mode='w', appdata=False, **kwargs):
        logger.debug('Writing ConfigParseBetter config.')
        filepath = self.createConfigPath(filepath, appdata) if filepath else self.__filepath
        encoding = kwargs.get('encoding', self.__encoding)
        with open(filepath, mode, encoding=encoding) as configfile:
            self.__parser.write(configfile)
        # -- Outdated version --
        #if (self.__autosave if autosave is None else autosave):     # attempt to auto-save all sections and their options
        #    for section_name in self.sections():
        #        for option in self.__parser.options(section_name):
        #            try:
        #                values = self.__dict__[section_name].__dict__[option]
        #                if type(values) in self.__iterTypes:    # unpack values
        #                    self.save(
        #                        option,
        #                        *values,
        #                        section=section_name
        #                    )
        #                else:                               # leave values as is
        #                    self.save(
        #                        option,
        #                        values,
        #                        section=section_name
        #                    )
        #            except KeyError: pass
        #            #section = self.__dict__[section_name]
        #            #section.__dict__[option] = section.__dict__[option]
        #    #for key, value in self.__dict__.items():
        #    #    if (key[:18] != '_configparsebetter' and
        #    #        not isinstance(value, BetterSectionProxy)):
        #    #        self.save(key, value)
        #with open(filepath, 'w') as configfile: self.__parser.write(configfile)

        # -- Twitch CPB version --
        #if (self.__autoSave if autoSave is None else autoSave):
        #    for section_name in self.sections():
        #        for option in self.__parser.options(section_name):
        #            try:
        #                info(section_name, option, self.__dict__[section_name].__dict__[option])
        #                self.save(
        #                    option,
        #                    self.__dict__[section_name].__dict__[option].value,
        #                    section=section_name
        #                )
        #            except KeyError: pass
        #            #section = self.__dict__[section_name]
        #            #section.__dict__[option] = section.__dict__[option]
        #    #for key, value in self.__dict__.items():
        #    #    if (key[:18] != '_configparsebetter' and
        #    #        not isinstance(value, BetterSectionProxy)):
        #    #        self.save(key, value)
        #path = self.createConfigPath(filepath, appdata) if filepath else self.__filepath
        #with open(path, 'w') as configfile: self.__parser.write(configfile)


    def refresh(self, newParser=None, autoread=True, **kwargs):
        ''' Deletes/replaces an old configparser object with a new one. '''
        oldSection = self.__dict__['_ConfigParseBetter__section'].name
        del self.__parser
        self.__parser = newParser or configparser.ConfigParser()  # TODO add the % thing here?
        if autoread:
            encoding = kwargs.get('encoding', self.__encoding)
            self.read(self.__filepath, encoding=encoding)
        self.setSection(oldSection)   # restore previous section, if possible


    def reset(self, ConfigParserObject=None, autoread=True):
        for key in self.__dict__:
            if key[:18] != '_ConfigParseBetter':
                del self.__dict__[key]
        self.refresh(ConfigParserObject, autoread)


    def read_dict(self, dictionary, *args, **kwargs):
        self.__parser.read_dict(dictionary, *args, **kwargs)


    def read_file(self, file, *args, **kwargs):
        self.__parser.read_file(file, *args, **kwargs)


    def read_string(self, string, *args, **kwargs):
        self.__parser.read_string(string, *args, **kwargs)


    def load(self, key, fallback='', delimiter=None,        # TODO should delimiter_type and val_type switch places?
             val_type=None, delimiter_type=None,
             fallback_align=True, force_delimiter_type=True,
             min_len=None, max_len=None, fill_with_defaults=False,
             fill_with_fallback=False, default=None, section=None):

        if isinstance(fallback, type):          # fallback is a literal type, like "fallback=int"
            fallback_type = fallback
            #fallback = fallback()               # get default value for that type (i.e. int() = 0)
            fallback = ''
            if val_type is None:
                val_type = fallback_type
        else:
            fallback_type = type(fallback)

        #section, value = self._load(key, fallback, fallback_type, delimiter, section)

        # TODO This block here was originally a separate function called _load, but it's been moved here for optimization
        if key[:3] == '__': raise LockedNameException(key)
        section = self.getSection(section)
        if section.name in self.__parser.sections():
            try:
                #print('fallback_type', fallback_type)
                if fallback_type == bool:
                    value = section.getboolean(key, fallback=fallback)
                elif fallback_type == int:
                    value = section.getint(key, fallback=fallback)
                elif fallback_type == float:
                    value = section.getfloat(key, fallback=fallback)
                else:
                    if fallback_type in self.__iterTypes:     # TODO: converting to string and back (bad and stupid)
                        delimiter = delimiter if delimiter is not None else ','
                        fallback = delimiter.join(str(v) for v in fallback)
                        #print('new', key, delimiter, fallback)
                    value = section.get(key, fallback=fallback)
                    #print('ended with', value, fallback)
            except:
                value = fallback
        elif not self.__sectionLock:
            value = self._loadFromAnywhere(key, fallback)
        else:
            value = fallback    # TODO add elif for raising error here?

        section[key] = str(value).replace('%', '%%')   # 1.0595 sec/million TODO these % signs are for a nightmare https://stackoverflow.com/questions/46156125/how-to-use-signs-in-configparser-python
        logger.debug(f'Loading: key={key} -> value={value} ({type(value)}) | fallback={fallback} delim={delimiter} val_type={val_type} delim_type={delimiter_type}')

        #try:                                   # TODO throw more errors here
        true_value = value
        if not true_value and not fallback and delimiter_type is None and true_value == fallback:
            #print('not true_value and not fallback and true_value == fallback')
            key = key.lower()
            bsp = self.getBetterSectionProxy(section)
            option_proxy = OptionProxy(key, bsp, delimiter)
            self.__dict__[key] = option_proxy
            #self.__dict__[section.name].__dict__[key] = value
            bsp.__dict__[key] = true_value      # TODO should these all be value here and not true_value?
            #return option_proxy
            return true_value

        # no delimiter set -> check if fallback is an iterable. if not, we can safely apply val_type to true_value
        if delimiter is None:
            if fallback in self.__iterTypes:    # no delimiter but fallback is an iterable for some reason TODO or type(fallback) in self.__iterTypes?
                delimiter = ','
            if val_type:
                true_value = val_type(true_value)

        # double check if we have a delimiter yet -> is so, value is going to be split into a list
        if delimiter is not None:
            #fallback_type = type(value)         # TODO why was this called fallback_type?
            #fallback_type = type()
            #print(f'value={value} type={fallback_type} fallback={fallback} type={type(fallback)}')

            if delimiter_type is None:
                if fallback_type in self.__iterTypes:        # no delimiter_type set
                    delimiter_type = fallback_type
                #else:
                #    delimiter_type = list
            #_skip_first_element = fallback == '' and delimiter_type is not None     # fallback is an empty string, but a delimiter_type was specified
            #_skip_first_element = fallback == ''    # TODO
            _empty_fallback = fallback == ''
            try:
                #if delimiter_type in self.__iterTypes:  # we want the final value to be an array of some kind
                #    print('here!', delimiter_type, delimiter, value)
                #    #joined_value = delimiter.join(str(v) for v in value)
                #    #print('joined_value:', joined_value)
                #else:
                #    joined_value = str(value)
                #true_value = joined_value.split(delimiter)

                #true_value = (value if value else fallback).split(delimiter)        # TODO add option for preserving empty lists for `value`?
                if value != '': true_value = value.split(delimiter)
                elif not _empty_fallback: true_value = fallback.split(delimiter)
                else: true_value = []
                #if _skip_first_element: true_value = true_value[1:]                 # TODO you cannot have a list with '' as the only element because of this

                #print(f'ABOUT TO SPLIT VALUE: {value}', true_value)
                if val_type:
                    if self.__stripValues:  # strip string values
                        # strip and typecast values to val_type. if failed, fill in with default if specified, otherwise use val_type's default
                        for index, val in enumerate(true_value):
                            try: true_value[index] = val_type(val.strip())
                            except ValueError:
                                if val_type is int:     # TODO test speed of this vs. "if val_type is int and '.' in val" / should this be separate entirely?
                                    try: true_value[index] = int(float(val.strip()))    # int() cannot convert float strings such as "398.0"
                                    except ValueError: true_value[index] = default if default is not None else val_type()   # example: int() = 0
                    else:                   # leave values as-is
                        #print('else', true_value)
                        # typecast values to val_type. if failed, fill in with default if specified, otherwise use val_type's default
                        for index, val in enumerate(true_value):
                            try: true_value[index] = val_type(val)
                            except ValueError:
                                if val_type is int:     # TODO test speed of this vs. "if val_type is int and '.' in val" / should this be separate entirely?
                                    try: true_value[index] = int(float(val))            # int() cannot convert float strings such as "398.0"
                                    except ValueError: true_value[index] = default if default is not None else val_type()   # example: int() = 0

                #fallback_list = true_value     # TODO why was I using this?
                #print(f'before skip_first_element fallback="{fallback}"', key, fallback_type, _skip_first_element, delimiter_type, fallback_list)
                if _empty_fallback: fallback_list = []
                else: fallback_list = fallback.split(delimiter)

                #print('before fallback corrections', true_value, fallback_list)
                if fallback_align:
                    #print(1, true_value)
                    #print('fallback_align', min_len, max_len, value, fallback_list)
                    fill_with_fallback = not fill_with_defaults
                    max_len = len(fallback_list)
                    min_len = len(fallback_list)
                if min_len or max_len:              # TODO these if-statements could be simplified
                    #print(2, true_value)
                    #print(f'min_len={min_len}, max_len={max_len}')
                    if max_len:                     # TODO need a way to only take the last ones
                        true_value = true_value[:max_len]
                    #print(2.1, true_value)
                    if min_len and len(true_value) < min_len:
                        #print(2.15, true_value)
                        if fill_with_defaults:
                            #print(2.2, true_value)
                            while len(true_value) < min_len:
                                true_value.append(default)
                            #print(2.25, true_value)
                        elif fill_with_fallback:
                            #print(2.3, true_value)
                            true_value += fallback_list[len(true_value):]
                            #print(2.35, true_value, fallback_list)
                        else:
                            #print(2.4, true_value)
                            true_value = fallback_list
                #elif not min_len:                   # TODO does unpacking len1lists here really serve a purpose? also actually use unpacklen1lists here is so
                #    print(3, true_value)
                #    if len(true_value) == 1:
                #        true_value = true_value[0]
                #    #elif len(true_value) == 0:     # TODO ??????
                #    #    true_value = joined_value
                #print('\nend of try', true_value)

            except:                                 # TODO this ALL needs more testing
                print(f'Inner-load error - {traceback.format_exc()}')
                try: true_value = value.split(delimiter)
                except: true_value = value
            if delimiter_type in self.__iterTypes:  # TODO should this be less strict?
                try:
                    #print('delimiter_type being applied', true_value, delimiter_type)
                    true_value = delimiter_type(true_value)
                    if not isinstance(true_value, delimiter_type):
                        raise TypeError
                except TypeError:
                    if   delimiter_type == list:  true_value = [true_value]
                    elif delimiter_type == tuple: true_value = (true_value,)
                    elif delimiter_type == set:   true_value = {true_value}
        key = key.lower()
        #section_proxy = self.__dict__[section.name]

        bsp = self.getBetterSectionProxy(section)  # TODO redundant? see below
        if key in bsp:                             # TODO this vs. __dict__ performance
            #option_proxy = bsp[key]                # TODO this vs. __dict__ performance
            #print('getting very real value from key', key, '->', bsp[key])
            #bsp[key].set(true_value)
            #print(key, self.__dict__)
            #print(key, self.__dict__[key])
            self.__dict__[key].set(true_value)
            #option_proxy.set(true_value)
        else:
            #option_proxy = OptionProxy(self, bsp, key, true_value)  # <- bad twitch CPB OptionProxies
            option_proxy = OptionProxy(key, bsp, delimiter)
            self.__dict__[key] = option_proxy
            #print('adding very real value to key', key, '->', true_value)
            bsp.__dict__[key] = true_value
            #print(bsp[key], bsp)
        #option_proxy = OptionProxy(key, bsp, delimiter)
        #self.__dict__[key] = option_proxy   # TODO is this line needed inside or outside the else-statement?
        #self.__dict__[key] = section  # 0.1276 sec/million
        #bsp.__dict__[key] = true_value
        #return option_proxy

        return true_value
        #except Exception as error: print(f'Outer-load error - {type(error)}: {error}')


    def loadFrom(self, section, key, fallback='', *args, **kwargs):
        return self.load(key, fallback, *args, section=section, **kwargs)


    def loadAllFromSection(self, section=None, fallback='',
                           name=None, returnKey=False):
        # TODO: If load() is called before setSection(), this will start
        #       returning the settings loaded without a section, even
        #       though they should be loaded into the 'DEFAULT' section.
        section = self.getSection(section)
        if name:
            for sectionKey in self.__parser.options(section.name):
                if sectionKey.startswith(name):
                    if returnKey:
                        yield sectionKey, self.load(sectionKey, fallback, section=section)
                    else:
                        yield self.load(sectionKey, fallback, section=section)
        else:
            for sectionKey in self.__parser.options(section.name):
                if returnKey:
                    yield sectionKey, self.load(sectionKey, fallback, section=section)
                else:
                    yield self.load(sectionKey, fallback, section=section)


    #def _load(self, key, fallback, fallback_type, delimiter, section=None, verifySection=True):
    #    if key[:3] == '__':
    #        raise LockedNameException(key)
    #    if verifySection:
    #        section = self.getSection(section)
    #    if section.name in self.__parser.sections():
    #        try:
    #            #if isinstance(fallback, type):              # fallback is a literal type, like "fallback=int"
    #            #    fallback_type = fallback
    #            #    fallback = fallback()                   # get default value for that type (i.e. int() = 0)
    #            #else:
    #            #    fallback_type = type(fallback)
#
    #            if fallback_type == bool:
    #                return section, section.getboolean(key, fallback=fallback)
    #            elif fallback_type == int:
    #                return section, section.getint(key, fallback=fallback)
    #            elif fallback_type == float:
    #                return section, section.getfloat(key, fallback=fallback)
    #            elif fallback_type in self.__iterTypes:     # TODO: converting to string and back (bad and stupid)
    #                delimiter = delimiter if delimiter is not None else ','
    #                fallback = delimiter.join(str(v) for v in fallback)
    #            #print(3, 'section', section, 'key', key, 'fallback', fallback, fallback_type)
    #            #print(4, section.get(key, fallback=fallback))
    #            return section, section.get(key, fallback=fallback)
    #        except:
    #            return section, fallback
    #    elif not self.__sectionLock:
    #        return section, self._loadFromAnywhere(key, fallback)
    #    else:
    #        return section, fallback    # TODO add elif for raising error here?


    def _loadFromAnywhere(self, key, fallback):     # TODO this is probably bad
        for section in self.__parser.sections():
            for sectionKey in self.__parser.options(section):
                if sectionKey == key.lower():
                    return self.__parser[section][sectionKey]
        return fallback


    def save(self, key, *values, delimiter=None,
             delimiter_type=None, section=None):
        logger.debug(f'Saving: key={key} values={values}, delim={delimiter}')
        if delimiter is None: delimiter = self.__defaultDelimiter
        if isinstance(values, generator): values = tuple(values)    # turn generator into more flexible iterable
        if self.__autoUnpackLen1Lists:
            if len(values) == 1 and type(values[0]) in self.__iterTypes:
                values = values[0]

        section = self.getSection(section)
        valueStr = delimiter.join(str(v).replace('%', '%%') for v in values)    # TODO more % stuff
        #valueStr = delimiter.join(str(v) for v in values)                      # <- original
        #section[key] = valueStr     # TODO do time test here
        self.__parser.set(section.name, key, valueStr)
        if delimiter_type is None:
            if len(values) == 1: self.__dict__[key.lower()].set(values[0])
            else: self.__dict__[key.lower()].set(values)
        else: self.__dict__[key.lower()].set(delimiter_type(values))
        #if delimiter_type is None and len(values) == 1:    # TODO delete this if the above works as expected
        #    self.__dict__[key.lower()] = values[0]
        #elif delimiter_type is not None:
        #    self.__dict__[key.lower()] = delimiter_type(values)
        #else:
        #    self.__dict__[key.lower()] = values

        # TODO twitch CPB. I think this is from before I redid stuff like __setattr__
        #if delimiter_type is None and len(values) == 1:
        #    try: self.__dict__[key.lower()].set(values[0])
        #    except: self.__dict__[key.lower()] = values[0]
        #elif delimiter_type is not None:
        #    try: self.__dict__[key.lower()].set(delimiter_type(values))
        #    except: self.__dict__[key.lower()] = delimiter_type(values)
        #else:
        #    try: self.__dict__[key.lower()].set(values)
        #    except: self.__dict__[key.lower()] = values


    def saveTo(self, section, key, *values,
               delimiter=None, delimiter_type=None):
        if not delimiter: delimiter = self.__defaultDelimiter
        self.save(key, *values, delimiter=delimiter,
                  delimiter_type=delimiter_type, section=section)


    def sections(self, name=None):
        if name: self._sectionsByName(name)
        else: return self.__parser.sections()


    def _sectionsByName(self, name):
        for section in self.__parser.sections():
            if section.startswith(name):
                yield section


    def setSection(self, section, locked=False):    # TODO finish `locked` parameter
        self.__section = self.getSection(section)


    def getSection(self, section=None):             # could this be faster?
        # TODO test try/except vs if statements for checking for sections
        if section is None:
            if self.__section is None:
                try:
                    section = self.__parser['DEFAULT']
                except:
                    self.__parser['DEFAULT'] = {}
                    section = self.__parser['DEFAULT']
            else:
                section = self.__section
        if isinstance(section, configparser.SectionProxy):
            try:
                return section
            except KeyError:
                name = section.name.lower()     # TODO this is why all sections are lowercase. why did I do this?
                #name = section.name
                section = {}
                self.__dict__[name] = BetterSectionProxy(self, name)
                return section
        else:
            try:
                section = section.lower()
                if section not in self.__dict__:
                    self.__dict__[section] = BetterSectionProxy(self, section)
                return self.__parser[section]
            except KeyError:
                self.__parser[section] = {}
                self.__dict__[section] = BetterSectionProxy(self, section)
                return self.__parser[section]
        raise InvalidSectionError(section, 'getSection')    # TODO ???


    def removeSection(self, section):   # TODO is shortening this to one faster/worth it?
        section = self.getSection(section)
        self.__parser.remove_section(section.name)


    # TODO more aliases? or fewer? should aliases just be flat out copies to avoid overhead?
    def remove_section(self, section): self.removeSection(section)
    def deleteSection(self, section):  self.removeSection(section)
    def delete_section(self, section): self.removeSection(section)  # this one's kinda excessive


    def copySection(self, section, newSection, deleteOld=False):
        section = self.getSection(section)
        newSection = self.getSection(newSection)
        self.setSection(newSection)
        for key, value in section.items():
            self.__parser.set(newSection.name, key, value)
        if deleteOld:
            self.__parser.remove_section(section.name)


    def renameSection(self, section, newSection):   # TODO like above, should this be a copy, not alias?
        self.copySection(section, newSection, deleteOld=True)


    def setFilepath(self, filepath, appdata=False):
        self.__filepath = self.createConfigPath(filepath, appdata)


    def getFilepath(self):
        return self.__filepath


    def getParser(self):
        return self.__parser


    def getOptions(self, section):
        try:
            section = section if isinstance(section, str) else section.name
            return self.__parser.options(section)
        except:
            raise InvalidSectionError(section, 'getOptions')


    def getItems(self, section):
        try:
            section = section.lower() if isinstance(section, str) else section.name.lower()
            #section = section if isinstance(section, str) else section.name    # TODO <- original (twitch CPB)
            return self.__parser.items(section)
        except:
            raise InvalidSectionError(section, 'getItems')


    def getBetterSectionProxy(self, section=None):
        section = section if section else self.__section
        if isinstance(section, configparser.SectionProxy):  # TODO: counter-intuitive?
            section = section.name
        for bsp in self.getBetterSectionProxies():
            if bsp.name == section:
                return bsp


    def getBetterSectionProxies(self):  # TODO: only used once -> combine with above for performance?
        for val in self.__dict__.values():
            if isinstance(val, BetterSectionProxy):
                yield val


    def getConfigDictionary(self):
        #for key, val in self.__dict__.items():
        #    if isinstance(val, BetterSectionProxy):
        #        print(key, val.getSettings())
        return {key: val.getSettings() for key, val in self.__dict__.items()
                if isinstance(val, BetterSectionProxy)}


    def __getitem__(self, key):
        try: return self.__parser[key]
        except: return None


    def __setitem__(self, key, value):
        #self.__parser[key] = value       # this crashes if `val`'s type is unexpected
        self.__setattr__(key, value)


    # TODO these versions are from twitch CPB
    #def __getitem__(self, key):
    #    try: return self.__dict__[key]
    #    except:
    #        #try: return self.__parser[key]
    #        try: return self.__getattr__(key)
    #        except: return None

    #def __setitem__(self, key, value):
    #    #self.__parser[key] = value
    #    self.__setattr__(key, value)


    def __setattr__(self, name, value):             # TODO horrific performance?
        if name[:18] != '_ConfigParseBetter':
            if type(value) in self.__iterTypes:     # TODO is this part redundant?
                delimiter = self.__defaultDelimiter
                casted_value = delimiter.join(str(v) for v in value)
            else:
                casted_value = str(value)
            bsp = self.__dict__[name].section.name
            self.__parser.set(bsp, name, casted_value)
            self.__dict__[name.lower()].set(value)    # this is OptionProxy.set (I think)
            #self.save(name, value)                   # TODO for autowriting after saves
        else:
            self.__dict__[name] = value


    def __getattr__(self, name):
        ''' Handles getting attributes that don't exist in __dict__ yet. '''
        if not name.islower():
            try:
                name = name.lower()
                return self.__dict__[name]
            except:
                try:
                    return self.__dict__[name].__dict__[name]
                except:
                    pass
        if name in self.sections():
            return BetterSectionProxy(self, name)
        value = self._loadFromAnywhere(key=name, fallback=None)
        #self.__dict__[name.lower()] = OptionProxy(name.lower(), ) value
        return value


    def __contains__(self, other):      # TODO clean up __dict__ references (TODO x2... what did this mean?)
        return other in self.__dict__


    def __enter__(self):
        self.read()
        return self


    def __exit__(self, type, value, traceback):
        self.write()


    #def __repr__(self):                # TODO this causes __getattribute__ to break??
    #    outputs = []
    #    for section, options in self.getConfigDictionary().items():
    #        output = [f"   {section}:"]
    #        for key, value in options.items():
    #            output.append(f'      {key}: {value}')
    #        outputs.append('\n'.join(output))
    #    #outputs = (f'{k} = {json.dumps(v, indent=4)}\n' for k,v in self.getConfigDictionary().items())  # TODO finish this from twitch cpb
    #    newline = '\n\n'
    #    return f'[{self.getFilepath()}]\n\n{newline.join(outputs)}\n'


    def loadQt(self, *args, **kwargs):
        raise NotImplementedError('This class does not support Qt. Use the ConfigParseBetterQt class instead.')


    def saveQt(self, *args, **kwargs):
        raise NotImplementedError('This class does not support Qt. Use the ConfigParseBetterQt class instead.')




class ConfigParseBetter(_ConfigParseBetter):
    def __getattribute__(self, name):   # TODO __repr__ causes this to break??
        ''' Handles getting any attribute at all. '''
        attr = object.__getattribute__(self, name)
        #print('!!! getting attr', attr, isinstance(attr, OptionProxy))
        #return attr.sectionDict[attr.name] if isinstance(attr, OptionProxy) else attr
        return attr.value if isinstance(attr, OptionProxy) else attr


    def __setattr__(self, name, val):
        if isinstance(attr := self.__dict__.get(name), OptionProxy): attr.set(val)
        return super().__setattr__(name, val)




class ConfigParseBetterQt(ConfigParseBetter):   # TODO support Pyside and other PyQt versions
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)       # TODO check typical ram usage of autosave feature
        self.__widgets = [] if self._ConfigParseBetter__autosave else None  # https://stackoverflow.com/questions/47019802/inheriting-class-attribute-with-double-underscore


    def write(self, *args, **kwargs):
        logger.debug(f'Writing ConfigParseBetterQt config ({len(self.__widgets)} widgets saved).')
        if self._ConfigParseBetter__autosave:   # autosave widgets with their parameters before writing
            for parameters in reversed(self.__widgets):
                self.saveQt(
                    *parameters[0],
                    children=parameters[-6],
                    recursive=parameters[-5],
                    ignore=parameters[-4],
                    extraWidgets=parameters[-3],
                    getComboText=parameters[-2],
                    section=parameters[-1]
                )
        super().write(*args, **kwargs)          # write normally


    def loadQt(self, *widgets, children=True, recursive=True, ignore=tuple(), extraWidgets={}, getComboText=False, section=None):
        from PyQt5.QtWidgets import QCheckBox, QLineEdit, QSlider, QDial, QComboBox, \
            QRadioButton, QPushButton, QSpinBox, QDoubleSpinBox, QGroupBox, QKeySequenceEdit
        from PyQt5.QtGui import QKeySequence
        if type(ignore) not in self._ConfigParseBetter__iterTypes: ignore = (ignore,)    # ensure ignore parameter is an array
        section = self.getSection(section)
        if self._ConfigParseBetter__autosave:   # remember widget and parameters for autosaving later
            self.__widgets.append((widgets, children, recursive, ignore, extraWidgets, getComboText, section))
        logger.debug(f'Loading Qt values from {len(widgets)} widget(s)')

        # checkable qactions, font-combobox, datetime

        def actionCheckBox(check, name):        # not really worth shoving into a lambda
            if not check.isCheckable(): return
            if not check.isTristate(): check.setChecked(self.load(name, check.isChecked(), section=section))
            else: check.setCheckState(self.load(name, int(check.checkState()), section=section))

        actionValue = lambda w, name: w.setValue(self.load(name, w.value(), section=section))
        actionCheck = lambda w, name: w.setChecked(self.load(name, w.isChecked(), section=section)) if w.isCheckable() else None
        actions = {
            QSpinBox:         actionValue,      # reuse lambdas where applicable
            QDoubleSpinBox:   actionValue,
            QSlider:          actionValue,
            QDial:            actionValue,
            QRadioButton:     actionCheck,
            QGroupBox:        actionCheck,
            QPushButton:      actionCheck,
            QCheckBox:        actionCheckBox,
            QLineEdit:        lambda w, name: w.setText(self.load(name, w.text(), section=section)),
            QKeySequenceEdit: lambda w, name: w.setKeySequence(QKeySequence.fromString(self.load(name, w.keySequence().toString(), section=section))),
            QComboBox:        (lambda w, name: w.setCurrentText(self.load(name, w.currentText(), section=section))
                               if getComboText else w.setCurrentIndex(self.load(name, w.currentIndex(), section=section)))
        }

        _ignore = []                        # the true ignore list
        for widget_type in ignore:
            if widget_type in actions: del actions[widget_type]
            elif not isinstance(widget_type, str): _ignore.append(widget_type.objectName())
            else: _ignore.append(widget_type)
        for widget_type, (getter, setter) in extraWidgets.items():
            actions[widget_type] = lambda w, name: (getattr(w, setter)(
                self.load(name, getattr(w, getter)(), section=section))
            )

        def getWidget(widget, ignore):      # gets and loads a single widget
            if widget in ignore: return
            name = widget.objectName()
            if name[:3] == 'qt_' or not name or name in ignore: return                  # ignore qt_ prefixes -> special qt things
            widget_type = type(widget)
            if widget_type in actions: actions[widget_type](widget, name)

        def getChildren(widget, ignore):    # like getWidget, but recursive. defined separately for performance optimization
            for child in widget.children():
                if child in ignore: continue
                name = child.objectName()
                if name[:3] == 'qt_' or not name or name in ignore: continue            # ignore qt_ prefixes -> special qt things
                widget_type = type(child)
                if widget_type in actions: actions[widget_type](child, name)
                getChildren(child, ignore)

        for widget in widgets:
            getWidget(widget, _ignore)
            if children:
                if recursive: getChildren(widget, _ignore)
                else:
                    for child in widget.children():
                        if child in _ignore: continue
                        name = child.objectName()
                        if name[:3] == 'qt_' or not name or name in _ignore: continue   # ignore qt_ prefixes -> special qt things
                        widget_type = type(child)
                        if widget_type in actions: actions[widget_type](child, name)


    def saveQt(self, *widgets, children=True, recursive=True, ignore=tuple(), extraWidgets={}, getComboText=False, section=None):
        from PyQt5.QtWidgets import QCheckBox, QLineEdit, QSlider, QDial, QComboBox, \
            QRadioButton, QPushButton, QSpinBox, QDoubleSpinBox, QGroupBox, QKeySequenceEdit
        if type(ignore) not in self._ConfigParseBetter__iterTypes: ignore = (ignore,)  # ensure ignore parameter is an array
        section = self.getSection(section)

        actionValue = lambda w, name: self.save(name, w.value(), section=section)
        actionCheck = lambda w, name: self.save(name, w.isChecked(), section=section) if w.isCheckable() else None
        actions = {
            QSpinBox:         actionValue,
            QDoubleSpinBox:   actionValue,
            QSlider:          actionValue,
            QDial:            actionValue,
            QRadioButton:     actionCheck,
            QGroupBox:        actionCheck,
            QPushButton:      actionCheck,
            QCheckBox:        lambda w, name: self.save(name, w.checkState() if w.isTristate() else w.isChecked(), section=section),
            QLineEdit:        lambda w, name: self.save(name, w.text(), section=section),
            QKeySequenceEdit: lambda w, name: self.save(name, w.keySequence().toString(), section=section),
            QComboBox:        (lambda w, name: self.save(name, w.currentText(), section=section)
                               if getComboText else self.save(name, w.currentIndex(), section=section)),
        }

        _ignore = []
        for widget_type in ignore:
            if widget_type in actions: del actions[widget_type]
            elif not isinstance(widget_type, str): _ignore.append(widget_type.objectName())
            else: _ignore.append(widget_type)
        for widget_type, (getter, _) in extraWidgets.items():
            actions[widget_type] = lambda w, name: self.save(
                name, getattr(w, getter)(), section=section
            )

        def getWidget(widget, ignore):
            name = widget.objectName()
            if name[:3] == 'qt_' or not name or name in ignore: return                  # ignore qt_ prefixes -> special qt things
            widget_type = type(widget)
            if widget_type in actions: actions[widget_type](widget, name)

        def getChildren(widget, ignore):        # TODO is there a faster way to find these widgets by their objectNames?
            for child in widget.children():
                name = child.objectName()
                if not name or name[:3] == 'qt_' or name in ignore: continue            # ignore qt_ prefixes -> special qt things
                widget_type = type(child)
                if widget_type in actions: actions[widget_type](child, name)
                getChildren(child, ignore)

        for widget in widgets:
            getWidget(widget, _ignore)
            if children:
                if recursive: getChildren(widget, _ignore)
                else:
                    for child in widget.children():
                        name = child.objectName()
                        if not name or name[:3] == 'qt_' or name in _ignore: continue   # ignore qt_ prefixes -> special qt things
                        widget_type = type(child)
                        if widget_type in actions: actions[widget_type](child, name)
