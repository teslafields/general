# must use Python 2.7
import smbus
import MySQLdb
import string
import time
import os
from Tkinter import *
import tkMessageBox as msg
from time import gmtime, strftime

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)
address = 0x5
cmd     = 0
bytesrx = 11
bytestx = 15
RXbuff_i2c = ['','','','','','','','','','','','','','','','']
TXbuff_i2c = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

db = MySQLdb.connect(host="localhost",
			user="root",
			passwd="helicopterinho",
			db="sistema_supervisorio")
cur = db.cursor()

root = Tk()

check_as = IntVar()
check_si = IntVar()
check_pj = IntVar()
sz = StringVar()
angle = StringVar()
sp = StringVar()
sn = StringVar()
tempo = StringVar()
ampsp = StringVar()
ampsn = StringVar()
ampsz = StringVar()
freq = StringVar()
nome_usuario = StringVar()
t_min = StringVar()
t_seg = StringVar()
t_mseg = StringVar()

class MyAppCentral(Frame):

	def __init__(self, master):

		Frame.__init__(self,master)
		self.master = master
		self.init_window()

	def init_window(self):

		self.frame1 = Frame(self.master)
		self.frame1.grid(row=0, column=0, sticky=N+S+E+W)

		self.label = Label(self.frame1, text="Escolha uma opcao:", font="Verdana 16").grid(row=0,columnspan=5,sticky=N+S+E+W)

		self.photo1 = PhotoImage(file="supervi.gif")
		self.label1 = Label(self.frame1, image=self.photo1).grid(row=1,column=0,sticky=N+S+E+W)

		self.separa1 = Label(self.frame1, bd = 3, relief=SUNKEN).grid(column=1,row=1,rowspan=2,sticky=N+S+E+W)

		self.photo2 = PhotoImage(file="afund.gif")
		self.label2 = Label(self.frame1, image=self.photo2).grid(row=1,column=2,sticky=N+S+E+W)

		read_data_button = Button(self.frame1, text="SUPERVISORIO", command=self.init_supervisorio).grid(row=2, column=0,sticky=N+S+E+W)
		afund_button = Button(self.frame1, text="REALIZAR ENSAIO", command = self.init_afundamento).grid(row=2, column=2,sticky=N+S+E+W)
	
	def init_supervisorio(self):

		self.SWindow = Toplevel(self.master)
		self.app_s = MyAppSupervisorio(self.SWindow)		

	def init_afundamento(self):

		self.AWindow = Toplevel(self.master)
		self.app_a = MyAppAfundamento(self.AWindow)			


class MyAppAfundamento(Frame):

	def __init__(self, master):

		Frame.__init__(self,master)
		self.init_window()

	def init_window(self):
		
		sp.set('0')
		sz.set('0')
		sn.set('0')
		angle.set('0')
		tempo.set('0')
		ampsp.set('0')
		ampsn.set('0')
		ampsz.set('0')
		freq.set('0')
		t_min.set('0')
		t_seg.set('0')
		t_mseg.set('0')

		Label(self.master, text="Painel de Testes", font="Verdana 16").grid(row=0,column=0,columnspan=8,sticky=N+S+W+E)
		
		Label(self.master).grid(row=1)
		Label(self.master, text="Nome do Usuario:", font="Verdana 12").grid(row=2,columnspan=2,sticky=W)
		Label(self.master).grid(row=3)
		Entry(self.master, textvariable = nome_usuario, width = 12).grid(row=4,column=1,columnspan=2,sticky=N+S+E+W)
		
		Label(self.master).grid(row=5)
		Label(self.master, text="Dados de pre e pos-falta (amplitude, frequencia e sequencia zero):",font="Verdana 12").grid(row=6, columnspan=8,sticky=E)
		Label(self.master).grid(row=7)
		Label(self.master, text="SP:").grid(row=8, column=0,sticky=E)
		Label(self.master, text="SN:").grid(row=9, column=0,sticky=E)
		Entry(self.master, textvariable = ampsp, width = 4).grid(row=8,column=1,sticky=N+S+E+W)
		Entry(self.master, textvariable = ampsn, width = 4).grid(row=9,column=1,sticky=N+S+E+W)
		Label(self.master, text="%").grid(row=8, column=2,sticky=W)
		Label(self.master, text="%").grid(row=9, column=2,sticky=W)
		
		Label(self.master, text="Freq:").grid(row=8, column=3,sticky=E)
		Label(self.master, text="SZ:").grid(row=9, column=3,sticky=E)
		Entry(self.master, textvariable = freq, width = 4).grid(row=8,column=4,sticky=N+S+E+W)
		Entry(self.master, textvariable = ampsz, width = 4).grid(row=9,column=4,sticky=N+S+E+W)
		Label(self.master, text="Hz").grid(row=8, column=5,sticky=W)
		Label(self.master, text="%").grid(row=9, column=5,sticky=W)
		
		Label(self.master, text="Duracao:").grid(row=10, column=0,sticky=E)
		Entry(self.master, textvariable = t_min, width = 4).grid(row=10,column=1,sticky=N+S+E+W)
		Label(self.master, text="min").grid(row=10, column=2,sticky=W)
		Entry(self.master, textvariable = t_seg, width = 4).grid(row=10,column=3,sticky=N+S+E+W)
		Label(self.master, text="s").grid(row=10, column=4,sticky=W)
		Entry(self.master, textvariable = t_mseg, width = 4).grid(row=10,column=5,sticky=N+S+E+W)
		Label(self.master, text="ms").grid(row=10, column=6,sticky=W)
		
		c1 = Checkbutton(self.master, text = "Simetrico", variable = check_si, onvalue=1, offvalue=0,height=5,width=10)
		c1.grid(row=11,columnspan=3,sticky=N+S+E+W)
		c2 = Checkbutton(self.master, text = "Assimetrico", variable = check_as, onvalue=1, offvalue=0,height=5,width=10)		
		c2.grid(row=11,column=3,columnspan=3,sticky=N+S+E+W)
		c3 = Checkbutton(self.master, text = "Phase Jump", variable = check_pj, onvalue=1, offvalue=0,height=5,width=10)		
		c3.grid(row=11,column=6,columnspan=3,sticky=N+S+E+W)

		Label(self.master, text="Dados do Afundamento:",font="Verdana 12").grid(row=12, columnspan=8,sticky=W)
		Label(self.master).grid(row=13)
		Label(self.master, text="SP:").grid(row=14, column=0,sticky=E)
		Label(self.master, text="SZ:").grid(row=14, column=3,sticky=E)
		Label(self.master, text="SN:").grid(row=15, column=0,sticky=E)
		Label(self.master, text="Angulo:").grid(row=15, column=3,sticky=E)
		Entry(self.master, textvariable = sp, width = 4).grid(row=14,column=1,sticky=N+S+E+W)
		Entry(self.master, textvariable = sz, width = 4).grid(row=14,column=4,sticky=N+S+E+W)
		Entry(self.master, textvariable = sn, width = 4).grid(row=15,column=1,sticky=N+S+E+W)
		Entry(self.master, textvariable = angle, width = 4).grid(row=15,column=4,sticky=N+S+E+W)
		Label(self.master, text="%").grid(row=14, column=2,sticky=W)
		Label(self.master, text="%").grid(row=14, column=5,sticky=W)
		Label(self.master, text="%").grid(row=15, column=2,sticky=W)
		Label(self.master, text="graus").grid(row=15, column=5,sticky=W)
		Label(self.master, text="Duracao:").grid(row=16, column=0,sticky=E)
		ee1 = Entry(self.master, textvariable = tempo, width = 4).grid(row=16,column=1,sticky=N+S+E+W)
		Label(self.master, text="ms").grid(row=16, column=2,sticky=W)
		
		Label(self.master).grid(row=17)
		Label(self.master).grid(row=19)
		Button(self.master, text="ON", bg="green", command=self.on).grid(row=18,rowspan=3, column=6,columnspan=2, sticky=N+S+E+W)
		Button(self.master, text="OFF", bg="red", command=self.off).grid(row=18,rowspan=3, column=0, sticky=N+S+E+W)
		Label(self.master).grid(row=20,column=10)
		
		#gerar_falta_button = Button(self.master, text="GERAR AFUNDAMENTO", bg="red", command = self.valida_afund)
		#gerar_falta_button.grid(row=9, column=2, columnspan=2,sticky=N+S+E+W)	
	
	def off(self):
	
		TXbuff_i2c = [219,0,0,0,0,0,0,0,0,0,0,0,0,0]
		bus.write_i2c_block_data(address,cmd,TXbuff_i2c)
		
	def on(self):

		try:
			myampsp = int(ampsp.get())
			myampsn = int(ampsn.get())
			myampsz = int(ampsz.get())
			myfreq = int(freq.get())
			mytmin = int(t_min.get())
			mytseg = int(t_seg.get())
			mytmseg = int(t_mseg.get())
			
			mysp = int(sp.get())
			mysn = int(sn.get())
			mysz = int(sz.get())
			myangle = int(angle.get())
			mytempo = int(tempo.get())
				
		except ValueError:
			msg.showinfo('Windows Tittle','Insira valores numericos')
			return
		
		if(myampsp > 100 or myampsp < 0 or myampsn > 100 or myampsn < 0 or myampsz > 100 or myampsz < 0 or myfreq < 0 or myfreq > 200 or mytmseg < 0 or mytmseg > 255 or mytmin < 0 or mytmin > 255 or mytseg < 0 or mytseg > 255):
			msg.showinfo('Windows Tittle','Dados de pre e pos-falta incorretos! Verificar restricoes')
		if (check_si.get() == 1 and check_as.get() == 1 and check_pj.get() == 1) or (check_si.get() == 0 and check_as.get() == 0 and check_pj.get() == 0) or (check_si.get() == 1 and check_as.get() == 1 and check_pj.get() == 0):
			msg.showinfo('Windows Tittle','Escolha SIMETRICO, ASSIMETRICO ou PHASE JUMP')

		elif ((check_si.get() == 1 and check_as.get() == 0 and check_pj.get() == 0)):
			if (mysp > 100) or mysp < 0 or mysn > 100 or mysn < 0 or mysz > 100 or mysz < 0 or myangle < 0 or myangle > 255:
				msg.showinfo('Windows Tittle','Sequencias positiva, negativa e zero definidas entre 0 e 100%, angulo entre 0 e 200 graus')
			elif mytempo < 0 or mytempo > 10000:
				msg.showinfo('Windows Tittle','1 < Tempo < 10000 ms')
			else:
				answer = msg.askquestion('Question 1','Confirmar ensaio?')
				if answer == 'yes':
					tempo_b1 = (mytempo&255)
					tempo_b2 = (mytempo&65280)>>8
					TXbuff_i2c = [0,mysp,mysn,mysz,myangle,tempo_b2,tempo_b1,myampsp,myampsn,myampsz,myfreq,mytmin,mytseg,mytmseg]
					
		
					time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
					
					#cur.execute("INSERT INTO Ensaio(user_name,desc_ensaio,data_ensaio) VALUES('"+nome_usuario.get()+"','S, SP: "+sp1.get()+", T: "+tempo.get()+"','"+time_now+"')")
					#cur.execute("SELECT MAX(ID_ensaio) FROM Ensaio WHERE user_name="+nome_usuario.get())
					#ID = cur.fetchone()
					#db.commit()
					print TXbuff_i2c
					print '####-Python->C-####'
					bus.write_i2c_block_data(address,cmd,TXbuff_i2c)
					bus.write_i2c_block_data(address,cmd,TXbuff_i2c)
					os.system('sudo ./demo '+tempo.get())

		elif ((check_si.get() == 0 and check_as.get() == 1 and check_pj.get() == 0)):
			if (mysp > 100) or mysp < 0 or mysn > 100 or mysn < 0 or mysz > 100 or mysz < 0 or myangle < 0 or myangle > 255:
				msg.showinfo('Windows Tittle','Sequencias positiva, negativa e zero definidas entre 0 e 100%, angulo entre 0 e 200 graus')
			elif mytempo < 0 or mytempo > 10000:
				msg.showinfo('Windows Tittle','1 < Tempo < 10000 ms')
			else:
				answer = msg.askquestion('Question 1','Confirmar ensaio?')
				if answer == 'yes':
					tempo_b1 = (mytempo&255)
					tempo_b2 = (mytempo&65280)>>8
					TXbuff_i2c = [1,mysp,mysn,mysz,myangle,tempo_b2,tempo_b1,myampsp,myampsn,myampsz,myfreq,mytmin,mytseg,mytmseg]
					
					time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		
					#cur.execute("INSERT INTO Ensaio(user_name,desc_ensaio,data_ensaio) VALUES('"+nome_usuario.get()+"','A, SP: "+sp2.get()+", SN: "+sn.get()+", T: "+tempo.get()+"','"+time_now+"')")
					#cur.execute("SELECT MAX(ID_ensaio) FROM Ensaio WHERE user_name="+nome_usuario.get())
					#ID = cur.fetchone()
					#db.commit()
					print TXbuff_i2c
					print '####-Python->C-####'
					bus.write_i2c_block_data(address,cmd,TXbuff_i2c)
					bus.write_i2c_block_data(address,cmd,TXbuff_i2c)
					os.system('sudo ./demo '+tempo.get())
		
		elif ((check_si.get() == 0 and check_as.get() == 0 and check_pj.get() == 1)):
			if (mysp > 100) or mysp < 0 or mysn > 100 or mysn < 0 or mysz > 100 or mysz < 0 or myangle < 0 or myangle > 255:
				msg.showinfo('Windows Tittle','Sequencias positiva, negativa e zero definidas entre 0 e 100%, angulo entre 0 e 200 graus')
			elif mytempo < 0 or mytempo > 10000:
				msg.showinfo('Windows Tittle','1 < Tempo < 10000 ms')
			else:
				answer = msg.askquestion('Question 1','Confirmar ensaio?')
				if answer == 'yes':
					tempo_b1 = (mytempo&255)
					tempo_b2 = (mytempo&65280)>>8
					TXbuff_i2c = [2,mysp,mysn,mysz,myangle,tempo_b2,tempo_b1,myampsp,myampsn,myampsz,myfreq,mytmin,mytseg,mytmseg]
					
					time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		
					#cur.execute("INSERT INTO Ensaio(user_name,desc_ensaio,data_ensaio) VALUES('"+nome_usuario.get()+"','A, SP: "+sp2.get()+", SN: "+sn.get()+", T: "+tempo.get()+"','"+time_now+"')")
					#cur.execute("SELECT MAX(ID_ensaio) FROM Ensaio WHERE user_name="+nome_usuario.get())
					#ID = cur.fetchone()
					#db.commit()
					print TXbuff_i2c
					print '####-Python->C-####'
					bus.write_i2c_block_data(address,cmd,TXbuff_i2c)
					bus.write_i2c_block_data(address,cmd,TXbuff_i2c)
					os.system('sudo ./demo '+tempo.get())
					
class MyAppSupervisorio(Frame):

	def __init__(self, master):

		Frame.__init__(self,master)
		self.init_window()

	def init_window(self):

		Label(self.master, text="Supervisorio do Conversor", font="Verdana 16").grid(row=0,column=0,columnspan=3,sticky=N+S+W+E)
		Label(self.master, text="Conversor A1").grid(row=2,  column=0,sticky=N+S+E+W)
		Label(self.master, text="Conversor A2").grid(row=4,  column=0,sticky=N+S+E+W)
		Label(self.master, text="Conversor A3").grid(row=6,  column=0,sticky=N+S+E+W)
		Label(self.master, text="Conversor B1").grid(row=2,  column=1,sticky=N+S+E+W)
		Label(self.master, text="Conversor B2").grid(row=4,  column=1,sticky=N+S+E+W)
		Label(self.master, text="Conversor B3").grid(row=6,  column=1,sticky=N+S+E+W)
		Label(self.master, text="Conversor C1").grid(row=2,  column=2,sticky=N+S+E+W)
		Label(self.master, text="Conversor C2").grid(row=4,  column=2,sticky=N+S+E+W)
		Label(self.master, text="Conversor C3").grid(row=6,  column=2,sticky=N+S+E+W)

		self.result1 = Text(self.master, width = 15, height = 1, wrap = WORD)
		self.result1.grid(row=3, column=0,sticky=N+S+E+W)

		self.result2 = Text(self.master, width = 15, height = 1, wrap = WORD)
		self.result2.grid(row=5, column=0,sticky=N+S+E+W)

		self.result3 = Text(self.master, width = 15, height = 1, wrap = WORD)
		self.result3.grid(row=7, column=0,sticky=N+S+E+W)

		self.result4 = Text(self.master, width = 15, height = 1, wrap = WORD)
		self.result4.grid(row=3, column=1,sticky=N+S+E+W)

		self.result5 = Text(self.master, width = 15, height = 1, wrap = WORD)
		self.result5.grid(row=5, column=1,sticky=N+S+E+W)

		self.result6 = Text(self.master, width = 15, height = 1, wrap = WORD)
		self.result6.grid(row=7, column=1,sticky=N+S+E+W)

		self.result7 = Text(self.master, width = 15, height = 1, wrap = WORD)
		self.result7.grid(row=3, column=2,sticky=N+S+E+W)

		self.result8 = Text(self.master, width = 15, height = 1, wrap = WORD)
		self.result8.grid(row=5, column=2,sticky=N+S+E+W)

		self.result9 = Text(self.master, width = 15, height = 1, wrap = WORD)
		self.result9.grid(row=7, column=2,sticky=N+S+E+W)
		fiforx_i2c = bus.read_i2c_block_data(address,cmd,bytesrx)
		print fiforx_i2c

	def read_I2C(self):	

		fiforx_i2c = bus.read_i2c_block_data(address,cmd,bytesrx)
		time.sleep(0.5)
		for i in range (0,len(fiforx_i2c)):
			RXbuff_i2c[i] = str(fiforx_i2c[i])

		print RXbuff_i2c
		self.show_screen()

			
root.wm_title("GUI Central")
gui = MyAppCentral(root)
root.mainloop()

db.close()
