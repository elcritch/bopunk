#!/usr/bin/python
import sys
import time
import shlex

class Variable:
    def __init__(self, name, type, value, default=None, min='', max=''):
        self.name = name
        self.type = type
        self.default = default
        self.min = min
        self.max = max
        self.set(value)
    
    def in_range(self, value):
        if self.type == 'string': return True
        if self.type == 'bool': return True
        if value < self.min or self.max < value:
            return False
        return True
    
    def set(self, value):
        try:
            if self.type == 'int':
                v = int(value)
                if not self.in_range(v):
                    return 'Value not in range'
                self.value = v
            
            elif self.type == 'bool':
                self.value = int(value) != 0
            
            elif self.type == 'real':
                v = float(value)
                if not self.in_range(v):
                    return 'Value not in range'
                self.value = v
            
            elif self.type == 'string':
                self.value = value
        
        except ValueError:
            return 'Invalid value for type'
    
    def __str__(self):
        s = self.name + ' ' + self.type + ' '
        if self.type == 'string':
            s += '"%s" "%s"'%(self.value,self.default)
        else:
            s += str(self.value) + ' '
            s += str(self.default) + ' '
            s += str(self.min) + ' '
            s += str(self.max) + ' '
        
        return s
        
    


class BoPunkSimulator:
    def __init__(self):
        self.buf = []
        self.is_open = 0
        self.line = ''
        self.firmware = 'A bunch of binary data: blah blah blah';
        self.uploading = False
        self.prompt()
        
        self.vars = {}
        
        self.add_var(Variable('Rate', 'int', 10, 15, 0, 100))
        self.add_var(Variable('Intensity', 'int', 150, 100, 0, 1000))
        self.add_var(Variable('Toggle', 'bool', False, False))
        self.add_var(Variable('Speed', 'real', 0.65, 0.5, 0, 1))
        self.add_var(Variable('SoundFile', 'string', 
            '/sounds/sound.wav','/sounds/sound.wav'))
    
    def add_var(self, var):
        self.vars[var.name] = var
    
    def check_open(self):
        if not self.open:
            raise Exception('not open')
    
    def open(self):
        self.is_open = 1
    
    def close(self):
        self.check_open()
        self.is_open = 0
    
    def read(self, count = 1):
        self.check_open()
        
        if not self.open:
            raise Exception('not open')
        
        s = ''
        while count and len(self.buf):
            s += self.buf.pop(0)
            count -= 1
        return s
    
    def readline(self):
        self.check_open()
        
        s = ''
        while len(self.buf):
            c = self.buf.pop(0)
            if c == '\n' or c == '\r':
                while len(self.buf) and (
                    self.buf[0] == '\n' or self.buf[0] == '\r'):
                    self.buf.pop(0)
                break
            s += c
        
        return s
    
    def write(self, s):
        self.check_open()
        
        for c in s:
            if self.uploading and self.up_size:
                self.up_size -= 1
                # Simulate delay
                if self.up_size & 100 == 0: time.sleep(0.01)
                self.firmware += c
                if self.up_size == 0:
                    self.uploading = 0
                    self.send('Ok\n')
                    self.prompt()
                continue
            
            if c == '\n' or c == '\r':
                if len(self.line):
                    args = shlex.split(self.line)
                    self.command(args[0], args)
                    self.line = ''
                if c == '\n' and not self.uploading:
                    self.prompt()
            
            else:
                self.line += c
    
    def send(self, s):
        self.buf.append(s)
    
    def prompt(self):
        self.send('> ')
    
    def splash(self):
        self.cmd_version()
    
    def cmd_list(self, args):
        self.send('<name> <type> <value> <default> [<min> <max>]\n')
        for v in self.vars.values():
            self.send(str(v) + '\n')
    
    def cmd_info(self, args):
        if len(args) != 2:
            self.send('\nInvalid Args\n')
        elif not args[1] in self.vars:
            self.send('\nInvalid Variable\n')
        else:
            self.send(str(self.vars[args[1]]) + '\n')

    
    def cmd_get(self, args):
        if len(args) != 2:
            self.send('\nInvalid Args\n')
        elif not args[1] in self.vars:
            self.send('\nInvalid Variable\n')
        else:
            self.send(str(self.vars[args[1]].value) + '\n')
    
    def cmd_set(self, args):
        if len(args) != 3:
            self.send('\nInvalid Args\n')
        elif not args[1] in self.vars:
            self.send('\nInvalid Variable\n')
        else:
            err = self.vars[args[1]].set(args[2])
            if err: self.send('\n' + err + '\n')
            else: self.send('Ok\n')
    
    def cmd_version(self, args = None):
        self.send('BoPunk\n')
        self.send('Protocol: 1.0\n')
        self.send('Firmware: 1.0\n')
        self.send('Title: A Cool BoPunk Firmware\n')
        self.send('ID: deadbeef\n')

    
    def cmd_reboot(self, args):
        time.sleep(1)
        self.splash()
    
    def cmd_upload(self, args):
        if len(args) != 2:
            self.send('\nInvalid Args\n')
        else:
            try:
                self.up_size = int(args[1])
                self.uploading = True
                self.firmware = ''
            
            except ValueError:
                self.send('\nInvalid Size\n')
    
    def cmd_download(self, args):
        self.send(str(len(self.firmware)) + '\n')
        self.send(self.firmware + '\n')
    
    def command(self, name, args):
        try:
            {'list':     self.cmd_list,
             'info':     self.cmd_info,
             'get':      self.cmd_get,
             'set':      self.cmd_set,
             'version':  self.cmd_version,
             'reboot':   self.cmd_reboot,
             'upload':   self.cmd_upload,
             'download': self.cmd_download,
             }[name](args)
        except KeyError:
            self.send('\nInvalid command\n')
            
        
    


def input():
    while 1:
        while 1:
            s = sim.read(1024)
            if s == '': break
            sys.stdout.write(s)
        
        line = sys.stdin.readline()
        if line == 'exit\n': break
        sim.write(line)
    
if __name__ == "__main__":
    sim = BoPunkSimulator()
    
    sim.open()
    
    s = sim.read(1024)
    sim.write('list\n')
    line = [s for s in sim.read(1024)]   
     
    sys.stdout.write(''.join(str(l) for l in line))
    
    # input()
    
    




