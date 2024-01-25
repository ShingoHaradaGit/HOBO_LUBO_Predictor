#Tsubasa Ito Chiba University

import sys, os, pickle, warnings
import tkinter as tk
from tkinter.font import Font
import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Avalon.pyAvalonTools import  GetAvalonFP 
from rdkit.Chem import Draw

#########################################################################################################################################################
warnings.simplefilter('ignore')
now_path = os.path.dirname(__file__)
sys.path.append(now_path)
fn_CHT = 4096
fn_EP = 4096
CHT_NCD_list = list(range(fn_EP))
EP_list = list(range(fn_EP))
##########################################################################################################################################################
class Window1(tk.Frame):

    def predict(self,txt1,txt2):
        CHT_smiles = str(txt1.get(1.0, tk.END+"-1c"))
        txt1.delete("1.0","end")
        EP_smiles = str(txt2.get(1.0, tk.END+"-1c"))
        txt2.delete("1.0","end")
        self.action = Window2(CHT_smiles, EP_smiles)

    def Exit(self):
        self.master.destroy()

    def __init__(self, master = None):
        super().__init__(master)
        # Setting of Text Area
        self.master.title(r"HOBO_LUBO_Predictor")
        self.master.geometry("300x190")

        # Setting of Fonts
        font1 = Font(family="Arial", size=14, weight=tk.font.BOLD, slant="italic")
        font2 = Font(family="Arial", size=12, weight=tk.font.BOLD)

        # Setting of Label
        label1 = tk.Label(self.master,text="CHT / NCD", font=font1)
        label2 = tk.Label(self.master,text="Enophile", font=font1)
        label1.place (x=110, y=5)
        label2.place (x=110, y=65)

        # Setting of CHT's SMILES Entry
        txt1 = tk.Text(height=2, width=38, bg="bisque", fg="black", font=font2)
        txt1.place(x=15, y=25)

        # Setting of EP's SMILES Entry
        txt2 = tk.Text(height=2, width=38, bg="bisque", fg="black", font=font2)
        txt2.place(x=15, y=85)

        # Setting of Predict Button
        bt_pred = tk.Button(text=u'Predict !!', bg ="pale green", height=1, width=10, font=font2, command=lambda:self.predict(txt1,txt2)) 
        bt_pred.place(x=30, y=140)

        # Setting of Exit Button
        bt_exit = tk.Button(self.master, text='Exit', bg="pale green", height=1, width=10, font=font2, command=lambda:self.Exit())
        bt_exit.place(x=160, y=140)

class Window2():

    @classmethod
    def Exit(cls, master=None):
        master.destroy()

    @classmethod
    def figure(cls,smiles):
        mols = [Chem.MolFromSmiles(smiles)]
        img = Draw.MolToFile(mols[0],'test.png', size=(200, 200))
        return img

    @classmethod
    def Result_window(cls, CHT_smiles, EP_smiles, list):
    
        CHT_HOBO = list[0]
        EP_LUBO = list[1]
        HOBO_LUBOGAP = list[2]

        CHT_HOBO = str(int(CHT_HOBO * 1000) / 1000)
        EP_LUBO = str(int(EP_LUBO * 1000) / 1000)
        HOBO_LUBOGAP = str(int(HOBO_LUBOGAP * 1000) / 1000)

        RESULT = tk.Toplevel()
        RESULT.title(r"Result")
        RESULT.geometry("430x350")

        # Setting of Fonts
        font3 = Font(family="Arial", size=15, weight=tk.font.BOLD, slant = "italic")
        font4 = Font(family="Arial", size=20, weight=tk.font.BOLD)

        bt_exit = tk.Button(RESULT, text='Exit', bg="pale green", height=1, width=10, font=font3, command=lambda:cls.Exit(master=RESULT))
        bt_exit.place(x=215, y=300, anchor=tk.CENTER)

        if not CHT_smiles == "" and EP_smiles == "":
            CHT_fig = cls.figure(CHT_smiles)
            CHT_fig = tk.PhotoImage(file = "test.png")
            CHT_canvas = tk.Label(RESULT, image = CHT_fig)
            CHT_canvas.place(x=215,y=120, anchor=tk.CENTER)
            os.remove("test.png")
            label_CHT = tk.Label(RESULT,text="CHT or NCD", font = font3)
            label_CHT_data = tk.Label(RESULT,text = str(CHT_HOBO) + " eV", font = font3)
            label_CHT.place (x=215, y=250, anchor=tk.CENTER)
            label_CHT_data.place (x=215, y=270, anchor=tk.CENTER)

        elif CHT_smiles == "" and not EP_smiles == "":
            EP_fig = cls.figure(EP_smiles)
            EP_fig = tk.PhotoImage(file = "test.png")
            EP_canvas = tk.Label(RESULT, image=EP_fig)
            EP_canvas.place(x=215,y=120, anchor=tk.CENTER)
            os.remove("test.png")
            label_EP = tk.Label(RESULT,text="Enophile", font = font3)
            label_EP_data = tk.Label(RESULT,text = str(EP_LUBO) + " eV", font = font3)
            label_EP.place (x=215, y=250, anchor=tk.CENTER)
            label_EP_data.place (x=215, y=270, anchor=tk.CENTER)

        elif CHT_smiles == "" or EP_smiles == "":
            warning_l = tk.Label(RESULT, text = "Please Input SMILES!!!", font = tk.font.Font(family="Arial", size=30, weight=tk.font.BOLD)) 
            warning_l.pack(expand = True)
        
        else:
            CHT_fig = cls.figure(CHT_smiles)
            CHT_fig = tk.PhotoImage(file = "test.png")
            CHT_canvas = tk.Label(RESULT, image = CHT_fig)
            CHT_canvas.place(x=10,y=10)
            os.remove("test.png")
            
            EP_fig = cls.figure(EP_smiles)
            EP_fig = tk.PhotoImage(file = "test.png")
            EP_canvas = tk.Label(RESULT, image=EP_fig)
            EP_canvas.place(x=220,y=10)
            os.remove("test.png")

            label_CHT = tk.Label(RESULT,text="CHT or NCD", font = font3) 
            label_EP = tk.Label(RESULT,text="Enophile", font = font3)
            label_GAP = tk.Label(RESULT, text="HOBO-LUBO GAP", font = font4) 
            label_CHT_data = tk.Label(RESULT,text = str(CHT_HOBO) + " eV", font = font3)
            label_EP_data = tk.Label(RESULT,text = str(EP_LUBO) + " eV", font = font3)
            label_GAP_data = tk.Label(RESULT, text = str(HOBO_LUBOGAP) + " eV", font = font4)  

            label_CHT.place (x=110, y=225, anchor=tk.CENTER)
            label_EP.place (x=325, y=225, anchor=tk.CENTER)
            label_GAP.place (x=215, y=268, anchor=tk.CENTER)
            label_CHT_data.place (x=110, y=245, anchor=tk.CENTER)
            label_EP_data.place (x=325, y=245, anchor=tk.CENTER)
            label_GAP_data.place (x=215, y=293, anchor=tk.CENTER)

            bt_exit.place(x=215, y=323, anchor=tk.CENTER)
        
        RESULT.mainloop()
    
    @classmethod
    def StoF(cls, smiles, fn):
        fingerprint = []
        fingerprints_SM = []
        safe = []

        mol = Chem.MolFromSmiles("")
        fp = GetAvalonFP(mol, fn)

        mols_list = [Chem.MolFromSmiles(smiles)]

        for s in fp.ToBitString():
            fingerprint.append(int(s))     

        for mol_idx, mol in enumerate(mols_list):
            try:
                fingerprint = [x for x in GetAvalonFP(mol, fn)]
                fingerprints_SM.append(fingerprint)
                safe.append(mol_idx)

            except:
                print("Error", mol_idx)
                continue
            
        fingerprints_SM = np.array(fingerprints_SM)
        df = pd.DataFrame(fingerprints_SM)

        return df

    def __init__(self, CHT_smiles, EP_smiles):
        try:
            CHT_fp = self.StoF(CHT_smiles, fn_CHT)
            EP_fp = self.StoF(EP_smiles, fn_EP)
        finally:

            CHT_fp = CHT_fp[CHT_NCD_list]
            EP_fp = EP_fp[EP_list]

            CHT_HOBO_model = pickle.load(open(now_path + '/CHTNCD_HOBO.pkl', 'rb'))
            EP_LUBO_model = pickle.load(open(now_path + '/EP_LUBO.pkl', 'rb'))

            CHT_HOBO = float(CHT_HOBO_model.predict(CHT_fp))
            EP_LUBO = float(EP_LUBO_model.predict(EP_fp))
            HOBO_LUBOGAP = float(EP_LUBO) - float(CHT_HOBO)
            Result_list = [CHT_HOBO, EP_LUBO, HOBO_LUBOGAP]

            self.Result_window(CHT_smiles, EP_smiles, Result_list,)

if __name__ =='__main__' :
    root = tk.Tk()
    window = Window1(master=root)
    window.mainloop()