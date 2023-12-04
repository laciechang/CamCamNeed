# -*- coding:utf-8 -*-
# Author: 张来吃
# Version: 1.0.1
# Contact: laciechang@163.com

# 2023.12.05 add Apple Log spec

# -----------------------------------------------------
# 本工具仅支持在达芬奇内运行 请将工具移至以下路径：
# macOS: /Users/{USER}/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Edit
# Windows: C:\Users\{USER}\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit
# -----------------------------------------------------

from PIL import Image, ImageDraw, ImageFont
import io
import base64
from datetime import datetime
import tempfile

Author = '' # 可在引号中填上你的名字就能每次以你的名字来生成，不填则会默认为「当前达芬奇项目的名字」
EXPORTFORMAT = '.png'

ResolveLogo = """
iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAAAEtGlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS41LjAiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6ZXhpZj0iaHR0cDovL25zLmFkb2JlLmNvbS9leGlmLzEuMC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIKICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIgogICAgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIKICAgZXhpZjpQaXhlbFhEaW1lbnNpb249IjI1NiIKICAgZXhpZjpQaXhlbFlEaW1lbnNpb249IjI1NiIKICAgZXhpZjpDb2xvclNwYWNlPSIxIgogICB0aWZmOkltYWdlV2lkdGg9IjI1NiIKICAgdGlmZjpJbWFnZUxlbmd0aD0iMjU2IgogICB0aWZmOlJlc29sdXRpb25Vbml0PSIyIgogICB0aWZmOlhSZXNvbHV0aW9uPSI3Mi8xIgogICB0aWZmOllSZXNvbHV0aW9uPSI3Mi8xIgogICBwaG90b3Nob3A6Q29sb3JNb2RlPSIzIgogICBwaG90b3Nob3A6SUNDUHJvZmlsZT0ic1JHQiBJRUM2MTk2Ni0yLjEiCiAgIHhtcDpNb2RpZnlEYXRlPSIyMDIz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
"""

RawLogo = """
iVBORw0KGgoAAAANSUhEUgAAAIAAAAA2CAYAAAAPrZGjAAAEsmlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS41LjAiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6ZXhpZj0iaHR0cDovL25zLmFkb2JlLmNvbS9leGlmLzEuMC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIKICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIgogICAgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIKICAgZXhpZjpQaXhlbFhEaW1lbnNpb249IjEyOCIKICAgZXhpZjpQaXhlbFlEaW1lbnNpb249IjU0IgogICBleGlmOkNvbG9yU3BhY2U9IjEiCiAgIHRpZmY6SW1hZ2VXaWR0aD0iMTI4IgogICB0aWZmOkltYWdlTGVuZ3RoPSI1NCIKICAgdGlmZjpSZXNvbHV0aW9uVW5pdD0iMiIKICAgdGlmZjpYUmVzb2x1dGlvbj0iNzIvMSIKICAgdGlmZjpZUmVzb2x1dGlvbj0iNzIvMSIKICAgcGhvdG9zaG9wOkNvbG9yTW9kZT0iMyIKICAgcGhvdG9zaG9wOklDQ1Byb2ZpbGU9InNSR0IgSUVDNjE5NjYtMi4xIgogICB4bXA6TW9kaWZ5RGF0ZT0iMjAyMy0w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
"""

CAMERASPECIFIC = {
    'Apple': {'colorspace': 'Apple Log / Rec. 2020', 'rawcodec': ''},
    'ARRI': {'colorspace': 'ARRI LogC3 / AWG', 'rawcodec':'ARRIRAW'},
    # 'ARRI': {'colorspace': 'ARRI LogC4 / AWG', 'rawcodec':'ARRIRAW'},
    'Canon':{'colorspace': 'Canon log2 / Cinema Gamut', 'rawcodec': 'Canon RAW'},
    'DJI': {'colorspace': 'D-Log / D-Gamut', 'rawcodec': 'DNG'},
    'Film': {'colorspace': 'Cineon', 'rawcodec': ''},
    'FUJIFILM': {'colorspace':  'F-Log / Rec. 2020', 'rawcodec': 'DNG'},
    'Nikon': {'colorspace': 'N-Log / Rec. 2020', 'rawcodec': 'Nikon RAW'},
    'Other':{'colorspace': 'Rec. 709', 'rawcodec': ''},
    'Panasonic':{'colorspace': 'VLog / VGamut', 'rawcodec': 'DNG'},
    'Phantom':{'colorspace': 'Log2', 'rawcodec': 'CINE'},
    'RED': {'colorspace': 'Log3G10 / REDWideGamutRGB', 'rawcodec': 'R3D'},
    'Sony':{'colorspace': 'Sony Slog3 / SGamut3.Cine', 'rawcodec': 'X-OCN'},
}

COLORMANAGEMENT = [
    'ACES',
    'RCM',
    'ALF',
    'TCAM',
    'ARRI REVEAL',
    'IPP2',
    'PFE',
    'YRGB',
]

def getCamera(clip):
    sourceItem = clip.GetMediaPoolItem()
    metadata = sourceItem.GetMetadata()
    try:
        return metadata['Camera Manufacturer']
    except KeyError:
        clipProperty = sourceItem.GetClipProperty()
        if 'X-OCN' in clipProperty['Video Codec']:
            return 'Sony'
        elif 'R3D' in clipProperty['Video Codec']:
            return 'RED'
        elif 'CINE' in clipProperty['Video Codec']:
            return 'Phantom'
        elif 'Canon' in clipProperty['Video Codec']:
            return 'Canon'
        elif 'Nikon' in clipProperty['Video Codec']:
            return 'Nikon'
        else:
            return 'Other'

def getColorManagement():
    global project
    scheme = {
        'davinciYRGBColorManagedv2': 'RCM',
        'acescc': 'ACES',
        'acescct': 'ACES',
        'davinciYRGB': 'YRGB'
    }
    settings = project.GetSetting()
    mode = settings['colorScienceMode']
    return scheme[mode]

def getRaw(clip):
    global CAMERASPECIFIC
    rawcodec = []
    for i in list(CAMERASPECIFIC.keys()):
        codec = CAMERASPECIFIC[i]['rawcodec']
        if codec != '':
            rawcodec.append(codec)
    
    sourceItem = clip.GetMediaPoolItem()
    clipProperty = sourceItem.GetClipProperty()
    if clipProperty['Video Codec'] in rawcodec or 'X-OCN' in clipProperty['Video Codec']:
        return True
    else:
        return False

def getColorspace(clip):
    global CAMERASPECIFIC
    camera = getCamera(clip)
    try:
        output = CAMERASPECIFIC[camera]['colorspace']
    except KeyError:
        CAMERASPECIFIC[camera] = {'colorspace':'', 'rawcodec': ''}
        output = ''
    return output

fu = bmd.scriptapp('Fusion')
ui = fu.UIManager
disp = bmd.UIDispatcher(ui)
resolve = bmd.scriptapp('Resolve')
project = resolve.GetProjectManager().GetCurrentProject()
timeline = project.GetCurrentTimeline()

UIAuthorName = 'UIAuthorName'
UIDate = 'UIDate'
UIWorkingSpace = 'UIWorkingSpace'
UICamera = 'UICamera'
UIRaw = 'UIRaw'
UIColorManagement = 'UIColorManagement'
OutputPick = 'OutputPick'
OutputPath = 'OutputPath'
OutputFileName = 'OutputFileName'
OutputFormat = 'OutputFormat'

if len(Author) == 0:
    AuthorName = project.GetName()
else:
    AuthorName = Author

window_01 = [
        ui.HGroup({"Spacing": 5},
        [
            ui.VGroup({"Spacing": 5, "Weight": 1},
            [
                ui.LineEdit({"ID": UIAuthorName, "Text": AuthorName}),
                ui.VGap(),
                ui.LineEdit({"ID": UIDate, "Text": datetime.now().strftime('%Y-%m-%d')}),
            ]),
            ui.VGroup({"Spacing": 5, "Weight": 1},
            [
                ui.ComboBox({"ID": UIWorkingSpace, 'Editable': True}),
                ui.HGroup([
                    ui.ComboBox({"ID": UICamera, 'Editable': True}),
                    ui.CheckBox({"ID": UIRaw, 'Text': 'RAW', "Weight": 0}),
                ]),
                ui.ComboBox({"ID": UIColorManagement, 'Editable': True}),
                
            ]),
            ui.Button({"ID": 'RUN', "Text": "📷", "Weight": 0.1}),
        ])
]

dlg = disp.AddWindow({ 
                        "WindowTitle": "📷 Cam Cam Need 📷", 
                        "ID": "MyWin", 
                        "Geometry": [ 
                                    600, 300, # position when starting
                                    800, 100 #width, height
                         ], 
                        "WindowFlags":{
                            "Window": True,
                        }
                        }, window_01)

itm = dlg.GetItems()

itm[UICamera].AddItems(list(CAMERASPECIFIC.keys()))
itm[UIColorManagement].AddItems(COLORMANAGEMENT)
itm[UIWorkingSpace].AddItems([ CAMERASPECIFIC[i]['colorspace'] for i in list(CAMERASPECIFIC.keys())])

itm[UIColorManagement].SetCurrentText(getColorManagement())
itm[UICamera].SetCurrentText(getCamera(timeline.GetCurrentVideoItem()))
itm[UIWorkingSpace].SetCurrentText(getColorspace(timeline.GetCurrentVideoItem()))
itm[UIRaw].Checked = getRaw(timeline.GetCurrentVideoItem())

def convertBase64(file):
    with open(file, 'rb') as file:
        data = file.read()
        imgdata = str(base64.b64encode(data), 'utf-8')
        print(imgdata)

class createStill(object):
    def __init__(self):
        self.inputImage = self.plateGen()
        self.font = 'PingFang.ttc'
        self.author = itm[UIAuthorName].Text
        self.date = datetime.now().strftime('%Y-%m-%d')

        self.width, self.height = self.inputImage.size
        if self.width > self.height:
            self.bannerHeight = int(self.height/4)
        else:
            self.bannerHeight = int(self.width/4)
        self.plateHeight = self.height + self.bannerHeight
        self.margin = int(self.width * 0.03)
        self.background = self.backgroundGen()
        self.draw = ImageDraw.Draw(self.background)
        self.lineHeight = self.bannerHeight * 0.134
        # self.BGColor = 63

    def plateGen(self):
        tmpFile = tempfile.NamedTemporaryFile(suffix=EXPORTFORMAT, delete=False)
        project.ExportCurrentFrameAsStill(tmpFile.name)
        return Image.open(tmpFile.name)
        
    def backgroundGen(self):
        background = Image.new('RGBA', (self.width, self.plateHeight), (63,63,63,255))
        return background
    
    def logoGen(self,logo):
        logoBytes = io.BytesIO(base64.b64decode(logo))
        logo = Image.open(logoBytes).convert('RGBA')
        return logo

    def paramGen(self, content: str, position: tuple, align='rm'):
        self.draw.text(xy=position, text=content, anchor=align ,fill=(255, 255, 255), font=self.fontGen('param'))

    def nameGen(self, name: str, position: tuple):
        self.draw.text(xy=position, text=name, anchor='lm' ,fill=(255, 255, 255), font=self.fontGen('name'))

    def fontGen(self, type = "param"):
        if type == 'param':
            return ImageFont.truetype(font=self.font, size=int(self.bannerHeight / 270 * 30))
        else:
            return ImageFont.truetype(font=self.font, size=int(self.bannerHeight / 270 * 50))
        
    def getParamList(self):
        return [
            itm[UIWorkingSpace].CurrentText,
            itm[UICamera].CurrentText, 
            itm[UIColorManagement].CurrentText + " ON", 
            ]
    
    def mainComp(self):
        self.background.paste(self.inputImage, (0,0))
        rawLogo = self.logoGen(RawLogo)

        paramBBox = self.fontGen('param').getbbox(max(self.getParamList(), key=len, default=""))
        paramWidth = paramBBox[2] - paramBBox[0]
        paramHeight = paramBBox[3] - paramBBox[1]
        rawSizeRatio = self.bannerHeight / 270 * 0.53
        rawLogo = rawLogo.resize((int(rawLogo.size[0]*rawSizeRatio), int(rawLogo.size[1]*rawSizeRatio)))

        if not itm[UIRaw].Checked:
            rawLogo = Image.new('RGBA', (0,0), (0,0,0,0))

        param1Height = int(self.height + self.bannerHeight/2 - self.lineHeight)
        param2Height = int(self.height + self.bannerHeight/2)
        param3Height = int(self.height + self.bannerHeight/2 + self.lineHeight)

        nameBBox = self.fontGen('name').getbbox(self.author)
        self.nameGen(self.author, (self.margin, param1Height + int((nameBBox[3] - nameBBox[1])*0.2) ))

        self.paramGen(self.getParamList()[0], (self.width - self.margin, param1Height)) # source colorspace
        self.paramGen(self.getParamList()[1], (int(self.width - self.margin - rawLogo.size[0]*1.2), param2Height)) # camera
        self.paramGen(self.getParamList()[2], (self.width - self.margin, param3Height)) # render scheme
        self.paramGen(self.date, (self.margin, param3Height), 'lm')
        
        resolveLogo = self.logoGen(ResolveLogo)
        logoSize = int(self.lineHeight*2 + paramHeight/2) #int(self.height / 1080 * 104)
        resolveLogo = resolveLogo.resize((logoSize, logoSize))
        
        logoOverlay = Image.new('RGBA', (self.width, self.plateHeight), (0,0,0,0))
        logoOverlay.paste(
            resolveLogo, 
            (
            int(self.width/2 - logoSize/2),
            # int(self.width - paramWidth - logoSize*1.5 - self.margin - rawLogo.size[0]*1.2), 
             int(self.height + self.bannerHeight/2 - resolveLogo.size[0]/2)
             ))
        print(rawLogo.size[0])
        logoOverlay.paste(
            rawLogo, 
            (self.width - self.margin - rawLogo.size[0], int(param2Height - rawLogo.size[1]/2)))
        result = Image.alpha_composite(self.background, logoOverlay)

        result.show()


def main():
    still = createStill()
    still.mainComp()

def _run(ev):
    main()

def _close(ev):
        disp.ExitLoop()

def _matchcolorspace(ev):
    who = ev['who']
    if who == UICamera:
        itm[UIWorkingSpace].SetCurrentText(CAMERASPECIFIC[itm[UICamera].CurrentText]['colorspace'])
    elif who == UIWorkingSpace:
        space = itm[UIWorkingSpace].CurrentText
        camera = [ i for i in list(CAMERASPECIFIC.keys()) if CAMERASPECIFIC[i]['colorspace'] == space][0]
        itm[UICamera].SetCurrentText(camera)

dlg.On[UICamera].CurrentIndexChanged = _matchcolorspace
dlg.On[UIWorkingSpace].CurrentIndexChanged = _matchcolorspace
dlg.On['RUN'].Clicked = _run
dlg.On.MyWin.Close = _close

dlg.Show()
disp.RunLoop()
dlg.Hide()