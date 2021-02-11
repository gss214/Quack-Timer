"""
Quack Timer
Desenvolvido por: Guilherme Silva Souza
https://github.com/gss214

MIT License

Copyright (c) 2021 Guilherme Silva Souza

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

from pydub import AudioSegment
from pydub.playback import play
import os
import sys
import tkinter as tk

class QuackTimer():
    def __init__(self):
        #Iniciando a UI
        self.root = tk.Tk()
        self.root.geometry("650x250")
        self.root.winfo_toplevel().title("QuackTimer")
        self.package_dir = os.getcwd()
        self.wav_path = self.find_data_file('quack_sound.wav')
        self.wav = AudioSegment.from_file(self.wav_path, format='wav')
        self.wav -= 10
        play(self.wav)

        self.seconds = 0
        self.is_running = False

        #Primeiro texto que vai ser exibido 
        self.title = tk.Label(self.root, text='Quack Timer')
        self.title.config(font=('helvetica', 14))
        self.title.pack(side='top')

        #Texto de instruções
        self.instruction_msg = tk.Label(
            self.root, text='Enter the time in seconds (greater than 0) to activate the QUACK')
        self.instruction_msg.config(font=('helvetica', 10))
        self.instruction_msg.pack(side='top')

        #Foto do pato
        self.duck_img = tk.PhotoImage(
            file=self.find_data_file('quackimage.png'))
        self.background_label = tk.Label(self.root, image=self.duck_img)
        self.background_label.pack()

        #Texto para se caso o usuario digite algo que nao eh um numero
        self.error_nan = tk.Label(
            self.root, text='that QUACK not QUACK is QUACK a QUACK number')
        self.error_nan.config(font=('helvetica', 10), background='red')
        
        self.error_negative_numer = tk.Label(
            self.root, text='Please QUACK enter QUACK a QUACK positive QUACK integer QUACK greater QUACK than QUACK 0')
        self.error_negative_numer.config(font=('helvetica', 10), background='red')

        #Texto para informar que o programa está rodando
        self.info_msg = tk.Label(self.root, text='running')
        self.info_msg.config(font=('helvetica', 10), background='blue')

        #Caixa do input
        self.input_user = tk.Entry(self.root)
        self.input_user.pack(side='top')

        #Botão para começar a rodar o programa
        self.start_bnt = tk.Button(self.root, text='start',
                            command=lambda: self.get_input())
        self.start_bnt.pack(side='top')

        #Botão para parar a execução do som
        self.stop_bnt = tk.Button(self.root, text='stop', command=lambda: self.stop())

        self.root.iconbitmap(self.find_data_file('quackimage.ico'))
        self.root.mainloop()

    def get_input(self):
        """
        A funcao get_input tenta pegar o input do usario, ela vai tentar
        converter o input para um inteiro, se nao conseguir vai retorna
        um valueerror e vai mostrar a msg pro usuario, se consegui ela
        verifica se o numero eh maior que 0, se for ela chama a funcao 
        para iniciar o loop onde vai tocar o som, se não ela retorna 
        mostrando uma mensagem de erro ao usuario.
        """
        try:
            self.seconds = int(self.input_user.get())
            if self.seconds <= 0:
                self.error_nan.pack_forget()
                self.error_negative_numer.pack()
                return
            self.input_user.pack_forget()
            self.instruction_msg.pack_forget()
            self.start_bnt.pack_forget()
            self.error_nan.pack_forget()
            self.error_negative_numer.pack_forget()
            self.info_msg.pack()
            self.stop_bnt.pack()
            self.is_running = True
            self.start()
        except ValueError:
            self.error_negative_numer.pack_forget()
            self.error_nan.pack(side='top')
            return

    def start(self):
        """
        A funcao start eh responsavel pelo loop onde vai tocar o som,  ela verifica
        se a variavel is_running eh True, se for ela toca o som
        """
        if self.is_running == True:
            play(self.wav)
        self.root.after(self.seconds * 1000, self.start)    
    
    def stop(self):
        """
        A funcao stop altera a variavel is running para false
        quebrando o loop principal que faz o som do pato tocar
        e volta a tela para a posicao inicial com a label de informacao,
        o input e o botao start visiveis.
        """
        self.is_running = False
        self.stop_bnt.pack_forget()
        self.info_msg.pack_forget()
        self.instruction_msg.pack()
        self.input_user.pack()
        self.start_bnt.pack()
        self.input_user.delete(0, 'end')


    def find_data_file(self, filename):
        """
        A funcao retorna o caminho do arquivo dentro da pasta resources

        Args:
            filename ([str]): o nome do arquivo completo

        Returns:
            [str]: retorna o caminho do arquivo.
        """
        if getattr(sys, 'frozen', False):
            datadir = os.path.dirname(sys.executable)
        else:
            datadir = os.path.dirname(__file__)
        return os.path.join(datadir, 'Resources', filename)

quack_timer = QuackTimer()
