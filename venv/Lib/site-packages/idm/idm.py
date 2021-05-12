import sys
import os
if not 'linux' in sys.platform:
    import comtypes.client as cc
else:
    import comtypes
import argparse
if sys.version_info.major == 2:
    input = raw_input

class IDMan(object):
    def __init__(self):
        super(IDMan, self)
        self.tlb = r'c:\Program Files\Internet Download Manager\idmantypeinfo.tlb'
        if not self.tlb:
            self.tlb = r'c:\Program Files\Internet Download Manager (x86)\idmantypeinfo.tlb'
        if not self.tlb:
            print("It seem IDM not installer, please install first !")
            sys.exit("It seem IDM not installer, please install first !")

    def get_from_clipboard(self):
        try:
            import clipboard
        except ImportError:
            print("Module Clipboard not Installer yet, please install first")
            q = input("Please re-input url download to:")
            if not q:
                sys.exit("You not input URL Download !")
            else:
                return q
        return clipboard.paste()

    def download(self, link, path_to_save=None, output=None, referrer=None, cookie=None, postData=None, user=None, password=None, confirm = False, lflag = None, clip=False):
        #print "link =", link
        #print "referrer =", referrer
        #print "postData =", postData
        #print "user     =", user
        #print "password =", password
        #print "path_to_save =", path_to_save
        #print "output   =", output
        #print "lflag    =", lflag

        if clip:
            link = self.get_from_clipboard()
        if confirm:
            lflag = 0
        else:
            lflag = 5
        try:
            cc.GetModule(['{ECF21EAB-3AA8-4355-82BE-F777990001DD}', 1, 0])
        except:
            cc.GetModule(self.tlb)

        import comtypes.gen.IDManLib as idman 
        idman1 = cc.CreateObject(idman.CIDMLinkTransmitter, None, None, idman.ICIDMLinkTransmitter2)
        if path_to_save:
            os.path.realpath(path_to_save)
        idman1.SendLinkToIDM(link, referrer, cookie, postData, user, password, path_to_save, output, lflag)

    def usage(self):
        parse = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        parse.add_argument('URL', action='store', help='url to download')
        parse.add_argument('-p', '--path', action='store', help='Path to save', default=os.getcwd())
        parse.add_argument('-o', '--output', help='Save with different name', action='store')
        parse.add_argument('-c', '--confirm', help='Confirm before download', action='store_true')
        parse.add_argument('-C', '--clip', help='Get URL from clipboard', action='store_true')
        if len(sys.argv) ==1:
            parse.print_help()
        else:
            args = parse.parse_args()
            self.download(args.URL, args.path, args.output, confirm=args.confirm, clip=args.clip)


if __name__ == '__main__':
    c = IDMan()
    c.usage()
