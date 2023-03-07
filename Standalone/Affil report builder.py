import customtkinter as ctk
import pandas as pd
import time
import sys
import os
from datetime import datetime, timedelta


class App(ctk.CTk):
    global resource

    def resource(relative_path):
        base_path = getattr(
            sys,
            '_MEIPASS',
            os.path.dirname(os.path.abspath(__file__))
        )
        return os.path.join(base_path, relative_path)

    def func(self, date:str = None):
        start_time = time.time()
        sep = ';'

        self.log.insert('insert', f'Chosen date is: {date}\n')
        userprofile = os.path.join(os.path.join(os.environ['USERPROFILE']))
        try:
            izzi = pd.read_csv(userprofile + "\\Downloads\\Affil_btag_Izzi.csv", sep=sep)
            jet = pd.read_csv(userprofile + "\\Downloads\\Affil_btag_Jet.csv", sep=sep)
            rox = pd.read_csv(userprofile + "\\Downloads\\Affil_btag_Rox.csv", sep=sep)
            fresh = pd.read_csv(userprofile + "\\Downloads\\Affil_btag_Fresh.csv", sep=sep)
            sol = pd.read_csv(userprofile + "\\Downloads\\Affil_btag_Sol.csv", sep=sep)
            volna = pd.read_csv(userprofile + "\\Downloads\\Affil_btag_Volna.csv", sep=sep)
            legzo = pd.read_csv(userprofile + "\\Downloads\\Affil_btag_Legzo.csv", sep=sep)
            starda = pd.read_csv(userprofile + "\\Downloads\\Affil_btag_Starda.csv", sep=sep)
            self.log.insert('insert', f'Starting...\n')
        except FileNotFoundError as e:
            self.log.insert('insert', e, tags='error')
            self.log.insert('insert', f'\nWaiting for input...\n')
            self.entry.delete(0, ctk.END)

        names = ['Izzi', 'Jet', 'Rox', 'Fresh', 'Sol', 'Volna', 'Legzo', 'Starda']

        projects = [izzi, jet, rox, fresh, sol, volna, legzo, starda]

        p_columns = [
            '% конверсии из регистрации в депозит', 'Hold', 'Подтверждение почты в %', 'Верификация тел в %',
            'VERIFIED документы %', '% женщин', '% молодежи', 'Deposit Sum>10000 %', 'Deposit Sum от 1K до 10K %',
            'Deposit Sum < 1000 %', '1 dep в %', 'От 5 fd %', 'LifeTime=0 дней %', 'LifeTime>7 дней %', '% успешных деп',
            'вывели средства от FD %', '% попыток вывода средств от FD (по игрокам)',
            '% реального вывода от запрошенного (по деньгам)', '% успешных OUT (по запросам)', '% бонусных ставок от общих',
            '% Не пользовались бонусами', '% совершали только бонусные ставки'
        ]
        t_columns = [
            'LifeTime', 'Количество депозитов успешных на человека', 'Количество депозитов на человека',
            'Q Ст отклонение 1 деп', 'Q bet/dep', 'Q Dep 7 дней', 'Q Dep 14 дней', 'Q Dep 30 дней',
            'Q Dep 60 дней', 'Q Dep 90 дней', 'Q Dep 120 дней', 'Q Dep 180 дней'
        ]
        # ------------------------------------------------------------------------------ #
        for project in projects:
            project.loc[project['Affil'].isnull(), 'Affil'] = 'No Affiliate'
            if 'Проект' in project.columns:
                project.drop('Проект', axis=1, inplace=True)
            for p_column in p_columns:
                project[p_column] = project[p_column].str.replace(',', '.').str.replace('%', '').astype('float') / 100
            for t_column in t_columns:
                project[t_column] = project[t_column].str.replace(',', '.').astype('float')

        with pd.ExcelWriter(
                userprofile + f"\\Desktop\\Affil_daily\\{date}.xlsx",
                engine_kwargs={
                    'options': {
                        'strings_to_numbers': True
                    }
                }
        ) as writer:
            for i in range(len(projects)):
                projects[i].to_excel(writer, sheet_name=names[i], index=False)
            workbook = writer.book

            pcent_format = workbook.add_format({'num_format': '0.0%'})
            for i, sheet in enumerate(writer.sheets.values()):
                (max_row, max_col) = projects[i].shape
                sheet.set_column(4, 4, width=40)
                sheet.set_column(9, 9, None, pcent_format)
                sheet.set_column(16, 16, None, pcent_format)
                sheet.set_column(25, 44, None, pcent_format)
                sheet.autofilter(0, 0, max_row, max_col - 1)
                sheet.autofilter(0, 0, max_row, max_col - 1)

            self.log.insert('insert', f'Document saved.\n', )

            if os.path.exists(userprofile + f"\\Desktop\\Affil_daily\\{date}.xlsx"):
                for name in names:
                    if os.path.exists(userprofile + f"\\Downloads\\Affil_btag_{name}.csv"):
                        os.remove(userprofile + f"\\Downloads\\Affil_btag_{name}.csv")
                    else:
                        self.log.insert('insert', f'Csv called {name} doesn\'t exist. Proceeding to the next.\n')
                        continue
            else:
                self.log.insert('insert', f'Summary file wasn\'t created. Check for errors.\n')

        self.log.insert('insert', "Execution took %s seconds.\n" % (time.time() - start_time))
        os.startfile((userprofile + f"\\Desktop\\Affil_daily"))

    def validate(self, key):
        try:
            inp = self.entry.get()
            date = (datetime.today() - timedelta(int(self.entry.get()))).strftime('%d.%m.%Y')
            self.func(date=date)
            self.entry.delete(0, ctk.END)
        except ValueError as e:
            self.log.insert('insert', f'{e}\n', tags='error')
            self.log.insert('insert', f'Please enter a number.\n')
            self.entry.delete(0, ctk.END)

    def __init__(self):
        super().__init__()

        self.title('Affil&Btag Builder')
        self.geometry('640x320')
        self.iconbitmap(resource('business-report.ico'))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        self.bind('<Return>', self.validate)

        self.title_label = ctk.CTkLabel(
            master=self,
            text="Enter number of days below:",
            font=ctk.CTkFont(family='<Roboto>',size=22, weight="normal")
        ).pack(
            padx=10,
            pady=(40, 20)
        )
        self.entry = ctk.CTkEntry(
            master=self,
            placeholder_text="For example: 1",
            width=500
        )
        self.entry.pack(pady=(0, 40))
        self.entry.after(1000, self.entry.focus_set)

        self.log = ctk.CTkTextbox(
            master=self,
            text_color='green',
            width=500,
            height=150
        )
        self.log.tag_add('error', '1.0', '1.end')
        self.log.tag_config('error', foreground='red')
        self.log.pack()


if __name__ == '__main__':
    app = App()
    app.mainloop()
