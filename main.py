import kivy
kivy.require('2.0.0')  
from kivy.app import App 
from kivy.uix.widget import Widget 
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.properties import ObjectProperty 
from kivy.lang import Builder 
from kivy.uix.popup import Popup 
from kivy.uix.floatlayout import FloatLayout 
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from glob import glob
import whirlpool
import hashlib
import threading
from kivy.clock import Clock
from progressspinner import ProgressSpinner
#Builder.load_file('login.kv') 
# -----------------------------------------------------------------------------
class file_Data():
    fullpath_filename = ''
    whirlpool_hash = ''
    sha256_hash = ''
    md5_hash = ''
    def __init__(self, fullname):
        self.fullpath_filename = fullname
    
    def getbasename(self):
        return os.path.basename(self.fullpath_filename)

    def compute_hash(self):
        hash_wp = 'Falha no calculo do hash whirlpool'
        hash_sha = 'Falha no calculo do hash sha256'
        hash_md5 = 'Falha no calculo do hash md5'
        try:
            with open(self.fullpath_filename,"rb") as f:
                data = f.read() # read file as bytes
                hash_wp = whirlpool.new(data).hexdigest()
                hash_sha = hashlib.sha256(data).hexdigest()
                hash_md5 = hashlib.md5(data).hexdigest()
        except:
            self.whirlpool_hash = hash_wp
            self.sha256_hash = hash_sha
            self.md5_hash = hash_md5
# -----------------------------------------------------------------------------      
class case_hash():
    req_number = 0
    fullpath_file_list = []
    def __init__(self):
        self.req_number = 0
# -----------------------------------------------------------------------------
currente_case_Hash = case_hash()
# -----------------------------------------------------------------------------
class windowManager(ScreenManager): 
    pass
# -----------------------------------------------------------------------------
# class RV(RecycleView):
#     def __init__(self, **kwargs):
#         super(RV, self).__init__(**kwargs)
#         # self.data = [{'text': str(x)} for x in range(100)]
# -----------------------------------------------------------------------------
class LoadDialog(FloatLayout):
    def MountScreen(self):
        self.clear_widgets()
        self.file_chooser = FileChooserListView()
        self.file_chooser.path = "/home/adelino"
        self.button_cancel = Button(text= "Cancelar")
        self.button_load = Button(text="Carregar") 
        main_layout = BoxLayout(orientation='vertical', size_hint=(1,1),
            pos_hint={"x":0.0, "top":1})
        button_layout = BoxLayout(size_hint_y= None, height= 30)
        button_layout.add_widget(self.button_cancel)
        button_layout.add_widget(self.button_load)
        main_layout.add_widget(self.file_chooser)
        main_layout.add_widget(button_layout)
        self.add_widget(main_layout)
        
    def __init__(self, **kwargs):
        super(LoadDialog, self).__init__(**kwargs)
        self.MountScreen()
# -----------------------------------------------------------------------------        
class loginWindow(Screen): 
    file_list = ObjectProperty(None) 
    num_files = ObjectProperty(None) 
    requisition = ObjectProperty(None)
    hashProgress = ProgressBar()
    tabLoad = FloatLayout()
    btn_enviar = ObjectProperty(None)
    vec_file_list = []
    sendProgress = ProgressSpinner(auto_start = False)
    # _popup = Popup(title="Save file",
    #                         size_hint=(0.9, 0.9))

    def MountScreen(self):
        # sendProgress = ProgressSpinner(size_hint=(0.075, 0.75),
                                    # pos_hint= {"x" : 0.025, "top" : 0.15} )
        # sendProgress = Label(text = "Qualquer coisa", size_hint=(0.075, 0.75),
        #                             pos_hint= {"x" : 0.025, "top" : 0.15} )
        # self.tabLoad.add_widget(sendProgress)
        return False
    #     tabPannel = TabbedPanel(size_hint = (.95, .95),
    #                 pos_hint= {'center_x': .5, 'center_y': .5}, do_default_tab= False)
    #     # ---
    #     tabLoad = TabbedPanelItem(text= 'Carregar')
    #     tabLoadLayout = FloatLayout(size= (1,1))
    #     tabLoadLayout.add_widget(Label(text= 'Número de requisição:', 
    #                                     halign= 'right',
    #                                     valign= 'middle',
    #                                     size_hint= (0.15, 0.05),
    #                                     pos_hint= {"x":0.05, "top":0.95} ))
    #     self.requisition = TextInput(multiline= False, size_hint= (0.15, 0.05),
    #                                     #size_hint_min= (150, 24),
    #                                     #size_hint_max= (150, 24),
    #                                 pos_hint= {"x" : 0.25, "top" : 0.95} )
    #     tabLoadLayout.add_widget(self.requisition)
    #     tabLoadLayout.add_widget(Label(text= 'Arquivos selecionados:',
    #                                     size_hint= (0.15, 0.05),
    #                                     pos_hint= {"x":0.5, "top":0.95} ))
    #     self.num_files = Label(text= '0',
    #                                     size_hint= (0.15, 0.05),
    #                                     pos_hint= {"x":0.75, "top":0.95} )
    #     tabLoadLayout.add_widget(self.num_files)
    #     self.load_dir = Button(size_hint= (0.2, 0.05), 
    #                     pos_hint= {"x" : 0.05, "top" : 0.85},
    #                     text= 'Carregar diretório...')
    #     self.load_dir.bind(on_release = lambda load_dir: self.show_load()) 
    #     tabLoadLayout.add_widget(self.load_dir)

    #     self.file_list = RecycleView(viewclass= 'myView', size_hint= (0.9, 0.60),
    #                                 pos_hint= {"x": 0.05, "top": 0.75})
    # #                 canvas.before:
    # #                     Color:
    # #                         rgba: (0.75,0.75,0.85,1)
    # #                     Rectangle:
    # #                         size: self.size
    # #                         pos: self.pos)
    #     RBL = RecycleBoxLayout(default_size= (None, 24), default_size_hint=(1, None),
    #                             size_hint_y= None, height= 24,
    #                             orientation= 'vertical')

    #     self.file_list.add_widget(RBL)
    #     tabLoadLayout.add_widget(self.file_list)
    #     tabLoad.add_widget(tabLoadLayout)
    #     tabPannel.add_widget(tabLoad)
    #     # ---
    #     tabBooking = TabbedPanelItem(text= 'Agendado')
        
    #     tabBookingLayout = FloatLayout(size= (1,1))
    #     tabBookingLayout.add_widget(Label(text= 'Em desenvolvimento'))
    #     tabBooking.add_widget(tabBookingLayout)
    #     tabPannel.add_widget(tabBooking)
    #     # ---
    #     self.add_widget(tabPannel)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog()
        self._popup = Popup(title="Carregar diretório", content=content,
                            size_hint=(0.9, 0.9))
        content.button_cancel.bind(on_release = lambda button_cancel: self.dismiss_popup())
        content.button_load.bind(on_release = lambda button_cancel: self.load(content.file_chooser.path,content.file_chooser.selection))
        self._popup.open()

    def load(self, path_choose, filename):
        self.vec_file_list = [str(y) for x in os.walk(path_choose) for y in glob(os.path.join(x[0], '*.*'))]
        result = [{'text': str(os.path.basename(y))}  for x in os.walk(path_choose) for y in glob(os.path.join(x[0], '*.*'))]
        # print("Diretório:",self.vec_file_list[0])
        self.file_list.data = result
        self.num_files.text = str(len(result))
        self.dismiss_popup()

    # def next(self, *largs):
    #     print("next, :",self.hashProgress.value,"/",self.hashProgress.max)
    #     if (self.hashProgress.value >= (self.hashProgress.max)):
    #         self.btn_enviar.disabled = False
    #         return False
    #     self.hashProgress.value += 1
    #     self.update_bar_trigger()

    def compute_hash_file_list(self,case_hash, hash_file_list, progress_bar):
        progress_bar.max=(len(hash_file_list)-1)
        progress_bar.value = 0
        for i in range(0,len(hash_file_list)):
            tempFileData = file_Data(hash_file_list[i])
            tempFileData.compute_hash()
            case_hash.fullpath_file_list.append(tempFileData)
            progress_bar.value += 1
            # self.hashProgress.value += 1
            #self.hashProgress.value = i
            # self.update_bar_trigger()
            # print("i:",progress_bar.value,"/",progress_bar.max)
        self.btn_enviar.disabled = False
        progress_bar.value = 0

    def hash_requisition(self):
        # Clock.schedule_interval(lambda dt:  self.next(), 1 / 100)
        global currente_case_Hash
        if (len(self.requisition.text) < 1):
            print("Entre com número de requisição válido")
            return 
        currente_case_Hash.req_number = int(self.requisition.text)
        currente_case_Hash.fullpath_file_list = []
        # self.hashProgress = ProgressBar()
        
        self.btn_enviar.disabled = True
        t1 = threading.Thread(target=self.compute_hash_file_list, args=(currente_case_Hash,self.vec_file_list, self.hashProgress))
        t1.start()
        
        

        # self.hashProgress.max=(len(self.vec_file_list)-1)
        # self.hashProgress.value = 0
        # for i in range(0,len(self.vec_file_list)):
        #     tempFileData = file_Data(self.vec_file_list[i])
        #     tempFileData.compute_hash()
        #     currente_case_Hash.fullpath_file_list.append(tempFileData)
        #     # self.hashProgress.value = i
        #     self.update_bar_trigger()
        #     print("i:",self.hashProgress.value,"/",self.hashProgress.max)

        # print(len(currente_case_Hash.fullpath_file_list))
        

    def __init__(self, *args, **kwargs):
        super(loginWindow, self).__init__(*args, **kwargs)
        # self.hashProgress = ProgressBar()
        # Clock.schedule_interval(lambda dt:  self.next(), 1 / 100)
        # self.update_bar_trigger = Clock.create_trigger(self.next,-1)
        # self.update_bar_trigger = Clock.schedule_interval(lambda dt: self.next, 1/30)
        # self.sendProgress.on_opacity(self,value=True)
        self.sendProgress = ProgressSpinner(auto_start = False)
        self.MountScreen()

# -----------------------------------------------------------------------------
class loginApp(App):     
    def build(self): 
        sm = windowManager() 
        # adding screens 
        sm.add_widget(loginWindow(name='login')) 
        return sm 
# -----------------------------------------------------------------------------
if __name__=="__main__": 
    loginApp().run()
