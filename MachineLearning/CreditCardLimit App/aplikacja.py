import tkinter as tk
from joblib import load
import csv
import os.path
from numpy import genfromtxt, where, size
import sys

font = ('Verdana', 12)
large_font = ('Verdana', 22, 'bold')
small_font = ('Verdana', 8)
model = 1

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

icon = resource_path('money.ico')
database = resource_path('CreditNumericOnly.csv')
rating_scaler = resource_path('scaler_rating.joblib')
limit_scaler = resource_path('scaler_limit.joblib')
rating_model_svr = resource_path('svr_model_rating.joblib')
limit_model_svr = resource_path('svr_model_limit.joblib')
rating_model_xgb = resource_path('xgb_model_rating.joblib')
limit_model_xgb = resource_path('xgb_model_limit.joblib')


class Credit(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Main)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class Main(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.focus_set(self)
        tk.Label(self, text='Kalkulator zdolności\nkredytowej', font=large_font).grid(row=0, sticky='nsew')
        tk.Label(self, text=' ', font=large_font).grid(row=1, sticky='nsew')
        tk.Label(self, text=' ', font=large_font).grid(row=2, sticky='nsew')
        tk.Label(self, text=' ', font=large_font).grid(row=3, sticky='nsew')
        tk.Label(self, text=' ', font=large_font).grid(row=4, sticky='nsew')
        tk.Label(self, text=' ', font=large_font).grid(row=5, sticky='nsew')
        tk.Label(self, text=' ', font=large_font).grid(row=6, sticky='nsew')
        tk.Button(self, text='Nowy klient (F1)', font=font,
                  command=lambda: master.switch_frame(New)).grid(row=4, sticky='nsew')
        tk.Button(self, text='Obecny klient (F2)', font=font,
                  command=lambda: master.switch_frame(Current)).grid(row=5, sticky='nsew')
        tk.Button(self, text='Wyjście (SHIFT + ESC)', font=font,
                  command=lambda: master.destroy()).grid(row=6, sticky='nsew')
        tk.Button(self, text='Ustawienia zaawansowane', font=font,
                  command=lambda: master.switch_frame(Options)).grid(row=11, sticky='nsew')
        tk.Label(self, text=' ', font=large_font).grid(row=7, sticky='nsew')
        tk.Label(self, text=' ', font=large_font).grid(row=8, sticky='nsew')
        tk.Label(self, text=' ', font=large_font).grid(row=9, sticky='nsew')
        tk.Label(self, text=' ', font=large_font).grid(row=10, sticky='nsew')
        tk.Label(self, text=' ', font=large_font).grid(row=12, sticky='nsew')
        tk.Label(self, text='made by: team Fajni', font=small_font).grid(row=13, sticky='nsew')
        tk.Frame.bind_all(self, sequence='<F1>', func=lambda x: master.switch_frame(New))
        tk.Frame.bind_all(self, sequence='<F2>', func=lambda x: master.switch_frame(Current))
        tk.Frame.bind_all(self, sequence='<Shift-Escape>', func=lambda x: master.destroy())


class New(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.focus_set(self)
        tk.Label(self, text='Nowy klient:', font=large_font).grid(row=0, columnspan=3)
        tk.Label(self, text=' ', font=font).grid(row=1, columnspan=3, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=4, columnspan=3, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=8, columnspan=3, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=11, columnspan=3, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=14, columnspan=3, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=17, columnspan=3, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=12, column=0, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=13, column=0, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=15, column=0, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=16, column=0, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=18, column=0, sticky='nsew')
        tk.Button(self, text='Menu główne (ESC)', font=font,
                  command=lambda: master.switch_frame(Main)).grid(row=18, columnspan=3, sticky='nsew')
        tk.Button(self, text='Reset (F6)', font=font,
                  command=lambda: self.reset(master)).grid(row=16, column=0, sticky='nsew')
        self.income = 0
        self.age = 0
        self.education = 0
        self.rating = 0
        self.sex = 2
        self.student = 2
        self.martial = 2
        self.ethnicity = 0
        self.rating_y = 3
        self.new_x_rating = [[0.0, 0, 0, 0, 0, 0, 0]]
        self.limit = 0
        self.new_x_limit = [[0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.popup_count = 0
        self.rating_count = 0
        tk.Frame.bind_all(self, sequence='<F4>', func=lambda x: self.predict_rating())
        tk.Frame.bind_all(self, sequence='<F5>', func=lambda x: self.save_file())
        tk.Frame.bind_all(self, sequence='<F6>', func=lambda x: self.reset(master))
        tk.Frame.bind_all(self, sequence='<Escape>', func=lambda x: master.switch_frame(Main))
        self.count_button()
        self.save_button()
        self.get_income()
        self.get_age()
        self.get_education()
        self.get_sex()
        self.get_student()
        self.get_martial_male()
        self.get_ethnicity()
        self.show_rating()
        self.show_limit()

    def load_model(self):
        self.scaler_rating = load(rating_scaler)
        self.scaler_limit = load(limit_scaler)
        if model == 1:
            self.model_rating = load(rating_model_svr)
            self.model_limit = load(limit_model_svr)
        elif model == 2:
            self.model_rating = load(rating_model_xgb)
            self.model_limit = load(limit_model_xgb)

    def check_save_button(self):
        if self.income != 0 and self.age != 0 and self.education != 0 and self.sex != 2\
                and self.student != 2 and self.martial != 2 and self.ethnicity != 0:
            self.save.destroy()
            self.save = tk.Button(self, text='Zapisz (F5)', command=self.save_file, font=font)
            self.save.grid(row=15, column=0, sticky='nsew')

    def save_file(self):
        if self.income != 0 and self.age != 0 and self.education != 0 and self.sex != 2 \
                and self.student != 2 and self.martial != 2 and self.ethnicity != 0 and self.rating_y != 3:
            if self.popup_count == 0:
                check_file = os.path.isfile('nowi_klienci.csv')
                if not check_file:
                    self.client_id = 501
                else:
                    my_data = genfromtxt('nowi_klienci.csv', delimiter=',')
                    last_id = my_data[-1][0]
                    self.client_id = int(last_id + 1)
                nowi_klienci = open('nowi_klienci.csv', 'a', newline='')
                columns = ['ClientID', 'Income', 'Rating', 'Limit', 'Age', 'Education', 'GenderNumeric',
                           'StudentNumeric', 'MarriedNumeric','EthnicityNumeric', 'Rating_Y']
                writer = csv.DictWriter(nowi_klienci, fieldnames=columns)
                if not check_file:
                    writer.writeheader()
                writer.writerow({'ClientID': self.client_id, 'Income': self.income, 'Rating': self.rating,
                                 'Limit': self.limit, 'Age': self.age,'Education': self.education,
                                 'GenderNumeric': self.sex, 'StudentNumeric': self.student,
                                 'MarriedNumeric': self.martial, 'EthnicityNumeric': self.ethnicity,
                                 'Rating_Y': self.rating_y})
                self.popup_save_message()
        else:
            pass

    def popup_save_message(self):
        self.popup_count = 1
        self.popup = tk.Toplevel()
        tk.Label(self.popup).pack()
        popup_text = 'Nowy numer klienta:'
        popup_id = self.client_id
        tk.Label(self.popup, text=popup_text, font=font).pack()
        tk.Label(self.popup, text=popup_id, font=large_font).pack()
        tk.Label(self.popup).pack()
        close = tk.Button(self.popup, text='OK', font=font, command=lambda: self.popup.destroy())
        close.pack()
        close.focus_set()
        close.bind('<Return>', self.popup_destroy)
        tk.Label(self.popup).pack()
        self.popup.geometry('250x160+10+10')
        self.popup.resizable(False, False)
        self.popup.title('Zapisano')
        self.save.destroy()
        self.save_button()
        self.popup.iconbitmap(icon)
        self.popup.grab_set()

    def popup_destroy(self, popup):
        self.popup.destroy()

    def save_button(self):
        self.save = tk.Button(self, text='Zapisz (F5)', font=font, state='disabled')
        self.save.grid(row=15, column=0, sticky='nsew')

    def reset(self, master):
        self.destroy()
        master.switch_frame(New)

    def count_button(self):
        self.count = tk.Button(self, text='Oblicz rating\noraz limit (F4)', font=font, state='disabled')
        self.count.grid(row=12, rowspan=2, column=0, sticky='nsew')

    def check_count_button(self):
        if self.income != 0 and self.age != 0 and self.education != 0 and self.sex != 2\
                and self.student != 2 and self.martial != 2 and self.ethnicity != 0:
            self.rating_count = 1
            self.count.destroy()
            self.count_active = tk.Button(self, text='Oblicz rating\noraz limit (F4)', font=font,
                                          command=self.predict_rating)
            self.count_active.grid(row=12, rowspan=2, column=0, sticky='nsew')
            self.popup_count = 0

    def get_income(self):
        income_validator = self.register(self.income_validation)
        income_label = tk.Label(self, text='Zarobki (pln):', font=font)
        income_label.grid(row=2, column=0)
        self.income_entry = tk.Entry(self, bd=3, validate='key', font=font, width=10,
                                     validatecommand=(income_validator, '%P'))
        self.income_entry.grid(row=3, column=0)
        self.income_entry.focus_set()
        self.income_entry.bind('<Return>', self.push_income)
        self.income_entry.bind('<FocusOut>', self.push_income)

    def push_income(self, event=None):
        if self.income_entry.get() == '':
            self.income = 0
        else:
            self.income = int(self.income_entry.get())
        self.new_x_rating[0][0] = (self.income / 100)
        self.new_x_limit[0][0] = (self.income / 100)
        self.check_count_button()

    def income_validation(self, income):
        try:
            if income == '' or int(income) in range(0, 9):
                return True
            elif int(income) and len(income) <= 7:
                return True
            else:
                raise ValueError
        except ValueError:
            self.bell()
            return False

    def get_age(self):
        age_validator = self.register(self.age_validation)
        age_label = tk.Label(self, text='Wiek:', font=font)
        age_label.grid(row=2, column=1)
        self.age_entry = tk.Entry(self, bd=3, validate='key', font=font, width=10,
                                  validatecommand=(age_validator, '%P'))
        self.age_entry.grid(row=3, column=1)
        self.age_entry.focus()
        self.age_entry.bind('<Return>', self.push_age)
        self.age_entry.bind('<FocusOut>', self.push_age)

    def push_age(self, event=None):
        if self.age_entry.get() == '':
            self.age = 0
        else:
            self.age = int(self.age_entry.get())
        self.new_x_rating[0][1] = self.age
        self.new_x_limit[0][2] = self.age
        self.check_count_button()

    def age_validation(self, age):
        try:
            if age == '':
                return True
            elif int(age) and len(age) < 3:
                return True
            else:
                raise ValueError
        except ValueError:
            self.bell()
            return False

    def get_education(self):
        education_validator = self.register(self.education_validation)
        education_label = tk.Label(self, text='Lata nauki:', font=font)
        education_label.grid(row=2, column=2)
        self.education_entry = tk.Entry(self, bd=3, validate='key', font=font, width=10,
                                        validatecommand=(education_validator, '%P'))
        self.education_entry.grid(row=3, column=2)
        self.education_entry.focus()
        self.education_entry.bind('<Return>', self.push_education)
        self.education_entry.bind('<FocusOut>', self.push_education)

    def push_education(self, event=None):
        if self.education_entry.get() == '':
            self.education = 0
        else:
            self.education = int(self.education_entry.get())
        self.new_x_rating[0][2] = self.education
        self.new_x_limit[0][3] = self.education
        self.check_count_button()

    def education_validation(self, education):
        try:
            if education == '':
                return True
            elif int(education) and len(education) < 3:
                return True
            else:
                raise ValueError
        except ValueError:
            self.bell()
            return False

    def get_sex(self):
        sex_label = tk.Label(self, text='Płeć:', font=font)
        sex_label.grid(row=5, column=0)
        self.sex_val = tk.IntVar(self, value=2)
        self.male_button = tk.Radiobutton(self, text='Mężczyzna', command=self.push_sex,
                                          font=font, variable=self.sex_val, value=1, indicatoron=1)
        self.male_button.grid(row=6, column=0)
        self.female_button = tk.Radiobutton(self, text='Kobieta', command=self.push_sex,
                                            font=font, variable=self.sex_val, value=0, indicatoron=1)
        self.female_button.grid(row=7, column=0)
        self.male_button.bind('<Return>', self.select_male)
        self.female_button.bind('<Return>', self.select_female)

    def push_sex(self, event=None):
        self.push_income()
        self.push_age()
        self.push_education()
        self.sex = int(self.sex_val.get())
        self.martial_sex()
        self.new_x_rating[0][3] = self.sex
        self.new_x_limit[0][4] = self.sex
        self.check_count_button()

    def select_male(self, male_button):
        self.male_button.invoke()
        self.push_income()
        self.push_age()
        self.push_education()

    def select_female(self, female_button):
        self.female_button.invoke()
        self.push_income()
        self.push_age()
        self.push_education()

    def get_student(self):
        student_label = tk.Label(self, text='Studia w trakcie:', font=font)
        student_label.grid(row=5, column=1)
        self.student_val = tk.IntVar(self, value=2)
        self.yes_button = tk.Radiobutton(self, text='Tak', command=self.push_student,
                                         font=font, variable=self.student_val, value=1, indicatoron=1)
        self.yes_button.grid(row=6, column=1)
        self.no_button = tk.Radiobutton(self, text='Nie', command=self.push_student,
                                        font=font, variable=self.student_val, value=0, indicatoron=1)
        self.no_button.grid(row=7, column=1)
        self.yes_button.bind('<Return>', self.select_yes)
        self.no_button.bind('<Return>', self.select_no)

    def push_student(self, event=None):
        self.push_income()
        self.push_age()
        self.push_education()
        self.student = int(self.student_val.get())
        self.new_x_rating[0][4] = self.student
        self.new_x_limit[0][5] = self.student
        self.check_count_button()

    def select_yes(self, yes_button):
        self.yes_button.invoke()
        self.push_income()
        self.push_age()
        self.push_education()

    def select_no(self, no_button):
        self.no_button.invoke()
        self.push_income()
        self.push_age()
        self.push_education()

    def martial_sex(self):
        self.trapped_button.destroy()
        self.free_button.destroy()
        if self.sex == 1:
            self.get_martial_male()
        if self.sex == 0:
            self.get_martial_female()

    def get_martial_male(self):
        martial_label = tk.Label(self, text='Stan cywilny:', font=font)
        martial_label.grid(row=5, column=2)
        self.martial_val = tk.IntVar(self, value=2)
        self.trapped_button = tk.Radiobutton(self, text='Żonaty', command=self.push_martial,
                                             font=font, variable=self.martial_val, value=1, indicatoron=1)
        self.trapped_button.grid(row=6, column=2)
        self.free_button = tk.Radiobutton(self, text='Kawaler', command=self.push_martial,
                                          font=font, variable=self.martial_val, value=0, indicatoron=1)
        self.free_button.grid(row=7, column=2)
        self.trapped_button.bind('<Return>', self.select_trapped)
        self.free_button.bind('<Return>', self.select_free)

    def get_martial_female(self):
        martial_label = tk.Label(self, text='Stan cywilny:', font=font)
        martial_label.grid(row=5, column=2)
        self.martial_val = tk.IntVar(self, value=2)
        self.trapped_button = tk.Radiobutton(self, text='Zamężna', command=self.push_martial,
                                             font=font, variable=self.martial_val, value=1, indicatoron=1)
        self.trapped_button.grid(row=6, column=2)
        self.free_button = tk.Radiobutton(self, text='Panna', command=self.push_martial,
                                          font=font, variable=self.martial_val, value=0, indicatoron=1)
        self.free_button.grid(row=7, column=2)
        self.trapped_button.bind('<Return>', self.select_trapped)
        self.free_button.bind('<Return>', self.select_free)

    def push_martial(self, event=None):
        self.push_income()
        self.push_age()
        self.push_education()
        self.martial = int(self.martial_val.get())
        self.new_x_rating[0][5] = self.martial
        self.new_x_limit[0][6] = self.martial
        self.check_count_button()

    def select_trapped(self, trapped_button):
        self.trapped_button.invoke()
        self.push_income()
        self.push_age()
        self.push_education()

    def select_free(self, free_button):
        self.free_button.invoke()
        self.push_income()
        self.push_age()
        self.push_education()

    def get_ethnicity(self):
        ethnicity_label = tk.Label(self, text='Etniczność:', font=font)
        ethnicity_label.grid(row=9, column=1)
        self.ethnicity_val = tk.IntVar(self, value=0)
        self.caucasian_button = tk.Radiobutton(self, text='Kaukaska', command=self.push_ethnicity,
                                             font=font, variable=self.ethnicity_val, value=1, indicatoron=1)
        self.caucasian_button.grid(row=10, column=0)
        self.asian_button = tk.Radiobutton(self, text='Azjatycka', command=self.push_ethnicity,
                                          font=font, variable=self.ethnicity_val, value=2, indicatoron=1)
        self.asian_button.grid(row=10, column=1)
        self.nigger_button = tk.Radiobutton(self, text='Afroamerykańska', command=self.push_ethnicity,
                                           font=font, variable=self.ethnicity_val, value=3, indicatoron=1)
        self.nigger_button.grid(row=10, column=2)
        self.caucasian_button.bind('<Return>', self.select_caucasian)
        self.asian_button.bind('<Return>', self.select_asian)
        self.nigger_button.bind('<Return>', self.select_nigger)

    def push_ethnicity(self, event=None):
        self.push_income()
        self.push_age()
        self.push_education()
        self.ethnicity = int(self.ethnicity_val.get())
        self.new_x_rating[0][6] = self.ethnicity
        self.new_x_limit[0][7] = self.ethnicity
        self.check_count_button()

    def select_caucasian(self, caucasian_button):
        self.caucasian_button.invoke()
        self.push_income()
        self.push_age()
        self.push_education()

    def select_asian(self, asian_button):
        self.asian_button.invoke()
        self.push_income()
        self.push_age()
        self.push_education()

    def select_nigger(self, nigger_button):
        self.nigger_button.invoke()
        self.push_income()
        self.push_age()
        self.push_education()

    def predict_rating(self):
        self.load_model()
        if self.rating_count == 1:
            x_new_rating_scaler = self.scaler_rating.transform(self.new_x_rating)
            y_new_rating = self.model_rating.predict(x_new_rating_scaler)
            if self.income < 1000 or self.age < 18 or self.education < 6:
                self.rating = 0
            else:
                self.rating = int(y_new_rating)
            self.new_x_limit[0][1] = self.rating
            self.show_rating_change()

    def show_rating(self):
        rating_label = tk.Label(self, text='Rating:  ', font=font)
        rating_label.grid(row=12, column=1, rowspan=2, sticky='e')
        self.rating_color = tk.LabelFrame(self, relief='raised', font=font)
        self.rating_color.grid(row=12, column=2, rowspan=2, sticky='nsew')
        self.rating_color_text = tk.Label(self.rating_color, text='0', font=large_font)
        self.rating_color_text.pack(expand=True, fill="none")

    def show_rating_change(self):
        self.rating_color.destroy()
        self.rating_color_text.destroy()
        if self.rating < 240:
            bg_color = 'red'
            self.rating_y = 0
        elif 240 <= self.rating <= 299:
            bg_color = 'yellow'
            self.rating_y = 1
        elif self.rating > 299:
            bg_color = 'green'
            self.rating_y = 2
        self.new_x_limit[0][8] = self.rating_y
        self.rating_color = tk.LabelFrame(self, relief='raised', font=font, bg=bg_color)
        self.rating_color.grid(row=12, column=2, rowspan=2, sticky='nsew')
        self.rating_color_text = tk.Label(self.rating_color, text=self.rating, font=large_font, bg=bg_color)
        self.rating_color_text.pack(expand=True, fill="none")
        self.predict_limit()

    def predict_limit(self):
        self.load_model()
        x_new_limit_scaler = self.scaler_limit.transform(self.new_x_limit)
        y_new_limit = self.model_limit.predict(x_new_limit_scaler)
        self.limit = int(y_new_limit)
        self.show_limit_change()

    def show_limit(self):
        limit_label = tk.Label(self, text='Maksymalny  \nlimit (pln):  ', font=font)
        limit_label.grid(row=15, column=1, rowspan=2, sticky='e')
        self.limit_color = tk.LabelFrame(self, relief='raised', font=font)
        self.limit_color.grid(row=15, column=2, rowspan=2, sticky='nsew')
        self.limit_color_text = tk.Label(self.limit_color, text='0', font=large_font)
        self.limit_color_text.pack(expand=True, fill="none")

    def show_limit_change(self):
        self.limit_color.destroy()
        self.limit_color_text.destroy()
        if self.rating_y == 0:
            limit_text = 0
        else:
            limit_text = self.limit
        self.limit_color = tk.LabelFrame(self, relief='raised', font=font)
        self.limit_color.grid(row=15, column=2, rowspan=2, sticky='nsew')
        self.limit_color_text = tk.Label(self.limit_color, text=limit_text, font=large_font)
        self.limit_color_text.pack(expand=True, fill="none")
        self.check_save_button()


class Current(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.focus_set(self)
        tk.Label(self, text='Obecny klient:', font=large_font).grid(row=0, columnspan=4)
        tk.Label(self, text=' ', font=font).grid(row=1, columnspan=4, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=4, columnspan=4, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=7, columnspan=4, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=10, columnspan=4, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=13, columnspan=4, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=14, column=0, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=15, column=0, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=17, column=0, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=18, column=0, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=16, columnspan=4, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=19, columnspan=4, sticky='nsew')
        tk.Button(self, text='Menu główne (ESC)', font=font,
                  command=lambda: master.switch_frame(Main)).grid(row=20, columnspan=4, sticky='nsew')
        tk.Button(self, text='Reset (F6)', font=font, command=lambda: self.reset(master)).grid(row=16, column=0,
                                                                                               sticky='nsew')
        self.clientid = ''
        self.extra_money_val = 0
        self.popup_count = 0
        self.income_editable = 0
        self.current_new_x_rating = [[0.0, 0, 0, 0, 0, 0, 0]]
        self.current_new_x_limit = [[0, 0, 0, 0, 0, 0, 0, 0, 0]]
        tk.Frame.bind_all(self, sequence='<F4>', func=lambda x: self.show_editable_income())
        tk.Frame.bind_all(self, sequence='<F5>', func=lambda x: self.save_file())
        tk.Frame.bind_all(self, sequence='<F6>', func=lambda x: self.reset(master))
        tk.Frame.bind_all(self, sequence='<Escape>', func=lambda x: master.switch_frame(Main))
        self.show_clientid()
        self.show_inactive_fields()
        self.save_button()

    def destroy_fields(self):
        self.old_limit.destroy()
        self.max_limit.destroy()
        self.extra_limit.destroy()
        self.income_entry.destroy()
        self.rating_entry.destroy()
        self.cards_entry.destroy()
        self.age_entry.destroy()
        self.education_entry.destroy()
        self.balans_entry.destroy()
        self.gender_entry.destroy()
        self.student_entry.destroy()
        self.married_entry.destroy()
        self.ethnicity_entry.destroy()

    def load_model(self):
        self.scaler_rating = load(rating_scaler)
        self.scaler_limit = load(limit_scaler)
        if model == 1:
            self.model_rating = load(rating_model_svr)
            self.model_limit = load(limit_model_svr)
        elif model == 2:
            self.model_rating = load(rating_model_xgb)
            self.model_limit = load(limit_model_xgb)

    def check_save_button(self):
        if self.extra_money_val !=0:
            self.save.destroy()
            self.save = tk.Button(self, text='Zapisz (F5)', command=self.save_file, font=font)
            self.save.grid(row=15, column=0, sticky='nsew')

    def save_file(self):
        if self.extra_money_val !=0:
            if self.popup_count == 0:
                check_file = os.path.isfile('obecni_klienci.csv')
                obecni_klienci = open('obecni_klienci.csv', 'a', newline='')
                columns = ['ClientID', 'Income', 'Rating', 'OldLimit', 'MaxLimit', 'Age', 'Education', 'GenderNumeric',
                           'StudentNumeric', 'MarriedNumeric','EthnicityNumeric']
                writer = csv.DictWriter(obecni_klienci, fieldnames=columns)
                if self.income_editable != 0:
                    csv_income = self.income_editable
                else:
                    csv_income = self.id_income.get()
                if not check_file:
                    writer.writeheader()
                writer.writerow({'ClientID': self.clientid, 'Income': csv_income, 'Rating': self.id_rating.get(),
                                 'OldLimit': self.old_limit_val, 'MaxLimit': self.current_new_limit,
                                 'Age': self.id_age.get(), 'Education': self.id_education.get(),
                                 'GenderNumeric': self.id_gender.get(), 'StudentNumeric': self.id_student.get(),
                                 'MarriedNumeric': self.id_married.get(),'EthnicityNumeric': self.id_ethnicity.get()})
                self.popup_save_message()
        else:
            pass

    def popup_save_message(self):
        self.popup_count = 1
        self.popup = tk.Toplevel()
        tk.Label(self.popup).pack()
        popup_text = 'Zapisano'
        tk.Label(self.popup, text=popup_text, font=font).pack()
        tk.Label(self.popup).pack()
        close = tk.Button(self.popup, text='OK', font=font, command=lambda: self.popup.destroy())
        close.pack()
        close.focus_set()
        close.bind('<Return>', self.popup_destroy)
        tk.Label(self.popup).pack()
        self.popup.geometry('160x110+10+10')
        self.popup.resizable(False, False)
        self.popup.title('Zapisano')
        self.save.destroy()
        self.save_button()
        self.popup.iconbitmap(icon)
        self.popup.grab_set()

    def popup_destroy(self, popup):
        self.popup.destroy()

    def save_button(self):
        self.save = tk.Button(self, text='Zapisz (F5)', font=font, state='disabled')
        self.save.grid(row=15, column=0, sticky='nsew')

    def reset(self, master):
        self.destroy()
        master.switch_frame(Current)

    def show_clientid(self):
        clientid_validator = self.register(self.clientid_validation)
        clientid_label = tk.Label(self, text='Numer klienta:', font=font)
        clientid_label.grid(row=2, column=0, columnspan=2)
        self.clientid_entry = tk.Entry(self, bd=3, validate='key', font=font, width=5,
                                       validatecommand=(clientid_validator, '%P'))
        self.clientid_entry.grid(row=3, column=0, columnspan=2)
        self.clientid_entry.focus()
        self.clientid_entry.bind('<Return>', self.push_clientid)
        self.clientid_entry.bind('<FocusOut>', self.push_clientid)

    def push_clientid(self, event=None):
        if self.clientid_entry.get() == '':
            self.save.destroy()
            self.destroy_fields()
            self.bell()
            self.save_button()
            self.show_inactive_fields()
        else:
            self.clientid = int(self.clientid_entry.get())
            my_data = genfromtxt(database, delimiter=',')
            self.find_row = my_data[where(my_data[:, 0] == self.clientid)]
            if size(self.find_row) > 0:
                self.show_fields()
                self.popup_count = 0
            else:
                self.save.destroy()
                self.destroy_fields()
                self.bell()
                self.save_button()
                self.show_inactive_fields()

    def clientid_validation(self, clientid):
        try:
            if clientid == '' or int(clientid) in range(0, 9):
                return True
            elif int(clientid) and len(clientid) <= 3:
                return True
            else:
                raise ValueError
        except ValueError:
            self.bell()
            return False

    def active_income_button(self):
        self.change_income_button.destroy()
        self.change_active_income_button = tk.Button(self, text='Edytuj\nzarobki (F4)',
                                                     font=font, command=self.show_editable_income)
        self.change_active_income_button.grid(row=2, column=2, rowspan=2)
        self.change_active_income_button.focus()

    def show_editable_income(self):
        if self.clientid != '':
            self.income_entry.destroy()
            self.income_entry_readonly.destroy()
            income_editable_validator = self.register(self.income_editable_validation)
            self.income_editable_entry = tk.Entry(self, bd=3, textvariable=self.id_income, validate='key', font=font,
                                                  width=9, validatecommand=(income_editable_validator, '%P'))
            self.income_editable_entry.grid(row=3, column=3)
            self.income_editable_entry.focus()
            self.income_editable_entry.bind('<Return>', self.push_editable_income)
            self.income_editable_entry.bind('<FocusOut>', self.push_editable_income)
        else:
            pass

    def push_editable_income(self, event=None):
        income_afteredit = tk.IntVar()
        if self.income_editable_entry.get() == '':
            self.income_editable = 0
            income_afteredit.set(0)
        else:
            self.income_editable = int(self.income_editable_entry.get())
            income_afteredit.set(self.income_editable_entry.get())
        self.income_editable_entry.destroy()
        self.income_editable_entry = tk.Entry(self, bd=3, textvariable=income_afteredit, font=font,
                                              width=9, state='readonly', justify='center')
        self.income_editable_entry.grid(row=3, column=3)
        self.current_new_x_rating[0][0] = (self.income_editable / 100)
        self.current_new_x_limit[0][0] = (self.income_editable / 100)
        self.predict_new_limit()
        self.popup_count = 0
        self.check_save_button()

    def income_editable_validation(self, income_editable):
        try:
            if income_editable == '' or int(income_editable) in range(0, 9):
                return True
            elif int(income_editable) and len(income_editable) <= 7:
                return True
            else:
                raise ValueError
        except ValueError:
            self.bell()
            return False

    def show_inactive_fields(self):
        self.change_income_button = tk.Button(self, text='Edytuj\nzarobki (F4)', font=font, state='disabled')
        self.change_income_button.grid(row=2, column=2, rowspan=2)
        income_label = tk.Label(self, text='Zarobki (pln):', font=font)
        income_label.grid(row=2, column=3)
        self.income_entry = tk.Entry(self, bd=3, font=font, width=9, state='disabled')
        self.income_entry.grid(row=3, column=3)
        rating_label = tk.Label(self, text='Rating:', font=font)
        rating_label.grid(row=5, column=0)
        self.rating_entry = tk.Entry(self, bd=3, font=font, width=9, state='disabled')
        self.rating_entry.grid(row=6, column=0)
        cards_label = tk.Label(self, text='Liczba kart:', font=font)
        cards_label.grid(row=5, column=1)
        self.cards_entry = tk.Entry(self, bd=3, font=font, width=9, state='disabled')
        self.cards_entry.grid(row=6, column=1)
        age_label = tk.Label(self, text='Wiek:', font=font)
        age_label.grid(row=5, column=2)
        self.age_entry = tk.Entry(self, bd=3, font=font, width=9, state='disabled')
        self.age_entry.grid(row=6, column=2)
        education_label = tk.Label(self, text='Lata nauki:', font=font)
        education_label.grid(row=5, column=3)
        self.education_entry = tk.Entry(self, bd=3, font=font, width=9, state='disabled')
        self.education_entry.grid(row=6, column=3)
        balans_label = tk.Label(self, text='Balans:', font=font)
        balans_label.grid(row=8, column=0)
        self.balans_entry = tk.Entry(self, bd=3, font=font, width=9, state='disabled')
        self.balans_entry.grid(row=9, column=0)
        gender_label = tk.Label(self, text='Płeć:', font=font)
        gender_label.grid(row=8, column=1)
        self.gender_entry = tk.Entry(self, bd=3, font=font, width=9, state='disabled')
        self.gender_entry.grid(row=9, column=1)
        student_label = tk.Label(self, text='Studia w trakcie:', font=font)
        student_label.grid(row=8, column=2)
        self.student_entry = tk.Entry(self, bd=3, font=font, width=9, state='disabled')
        self.student_entry.grid(row=9, column=2)
        married_label = tk.Label(self, text='Stan cywilny:', font=font)
        married_label.grid(row=8, column=3)
        self.married_entry = tk.Entry(self, bd=3, font=font, width=9, state='disabled')
        self.married_entry.grid(row=9, column=3)
        ethnicity_label = tk.Label(self, text='Etniczność:', font=font)
        ethnicity_label.grid(row=11, column=0)
        self.ethnicity_entry = tk.Entry(self, bd=3, font=font, width=14, state='disabled')
        self.ethnicity_entry.grid(row=12, column=0)
        old_limit_label = tk.Label(self, text='Obecny limit:', font=font)
        old_limit_label.grid(row=11, column=2, rowspan=2)
        self.old_limit = tk.LabelFrame(self, relief='raised')
        self.old_limit.grid(row=11, column=3, rowspan=2, sticky='nsew')
        max_limit_label = tk.Label(self, text='Maksymalny limit:', font=font)
        max_limit_label.grid(row=14, column=2, rowspan=2)
        self.max_limit = tk.LabelFrame(self, relief='raised')
        self.max_limit.grid(row=14, column=3, rowspan=2, sticky='nsew')
        extra_limit_label = tk.Label(self, text='Dostępne\nwolne środki:', font=font)
        extra_limit_label.grid(row=17, column=2, rowspan=2)
        self.extra_limit = tk.LabelFrame(self, relief='raised')
        self.extra_limit.grid(row=17, column=3, rowspan=2, sticky='nsew')

    def show_fields(self):
        self.destroy_fields()
        id_limit = tk.IntVar()
        id_limit.set(int(self.find_row[0][2]))
        limit_text = id_limit.get()
        self.old_limit_val = limit_text
        self.id_income = tk.DoubleVar()
        self.id_income.set(int(self.find_row[0][1] * 1000))
        self.current_new_x_rating[0][0] = (self.id_income.get() / 100)
        self.current_new_x_limit[0][0] = (self.id_income.get() / 100)
        self.id_rating = tk.IntVar()
        self.id_rating.set(int(self.find_row[0][3]))
        self.id_cards = tk.IntVar()
        self.id_cards.set(int(self.find_row[0][4]))
        self.id_age = tk.IntVar()
        self.id_age.set(int(self.find_row[0][5]))
        self.current_new_x_rating[0][1] = self.id_age.get()
        self.current_new_x_limit[0][2] = self.id_age.get()
        self.id_education = tk.IntVar()
        self.id_education.set(int(self.find_row[0][6]))
        self.current_new_x_rating[0][2] = self.id_education.get()
        self.current_new_x_limit[0][3] = self.id_education.get()
        self.id_balans = tk.IntVar()
        self.id_balans.set(int(self.find_row[0][7]))
        self.id_gender = tk.IntVar()
        self.id_gender.set(int(self.find_row[0][8]))
        self.current_new_x_rating[0][3] = self.id_gender.get()
        self.current_new_x_limit[0][4] = self.id_gender.get()
        self.id_student = tk.IntVar()
        self.id_student.set(int(self.find_row[0][9]))
        self.current_new_x_rating[0][4] = self.id_student.get()
        self.current_new_x_limit[0][5] = self.id_student.get()
        self.id_married = tk.IntVar()
        self.id_married.set(int(self.find_row[0][10]))
        self.current_new_x_rating[0][5] = self.id_married.get()
        self.current_new_x_limit[0][6] = self.id_married.get()
        self.id_ethnicity = tk.IntVar()
        self.id_ethnicity.set(int(self.find_row[0][11]))
        self.current_new_x_rating[0][6] = self.id_ethnicity.get()
        self.current_new_x_limit[0][7] = self.id_ethnicity.get()
        gender_text = tk.StringVar()
        if self.id_gender.get() == 1:
            gender_text.set('Mężczyzna')
        elif self.id_gender.get() == 0:
            gender_text.set('Kobieta')
        student_text = tk.StringVar()
        if self.id_student.get() == 1:
            student_text.set('Tak')
        elif self.id_student.get() == 0:
            student_text.set('Nie')
        married_text = tk.StringVar()
        if self.id_married.get() == 1:
            if self.id_gender.get() == 1:
                married_text.set('Żonaty')
            elif self.id_gender.get() == 0:
                married_text.set('Zamężna')
        elif self.id_married.get() == 0:
            if self.id_gender.get() == 1:
                married_text.set('Kawaler')
            elif self.id_gender.get() == 0:
                married_text.set('Panna')
        ethnicity_text = tk.StringVar()
        if self.id_ethnicity.get() == 1:
            ethnicity_text.set('Kaukaska')
        elif self.id_ethnicity.get() == 2:
            ethnicity_text.set('Azjatycja')
        elif self.id_ethnicity.get() == 3:
            ethnicity_text.set('Afroamerykańska')
        self.income_entry_readonly = tk.Entry(self, bd=3, font=font, width=9, state='readonly',
                                              textvariable=self.id_income, justify='center')
        self.income_entry_readonly.grid(row=3, column=3)
        rating_entry = tk.Entry(self, bd=3, font=font, width=9, state='readonly',
                                textvariable=self.id_rating, justify='center')
        rating_entry.grid(row=6, column=0)
        cards_entry = tk.Entry(self, bd=3, font=font, width=9, state='readonly',
                               textvariable=self.id_cards, justify='center')
        cards_entry.grid(row=6, column=1)
        age_entry = tk.Entry(self, bd=3, font=font, width=9, state='readonly',
                             textvariable=self.id_age, justify='center')
        age_entry.grid(row=6, column=2)
        education_entry = tk.Entry(self, bd=3, font=font, width=9, state='readonly',
                                   textvariable=self.id_education, justify='center')
        education_entry.grid(row=6, column=3)
        balans_entry = tk.Entry(self, bd=3, font=font, width=9, state='readonly',
                                textvariable=self.id_balans, justify='center')
        balans_entry.grid(row=9, column=0)
        gender_entry = tk.Entry(self, bd=3, font=font, width=9, state='readonly',
                                textvariable=gender_text, justify='center')
        gender_entry.grid(row=9, column=1)
        student_entry = tk.Entry(self, bd=3, font=font, width=9, state='readonly',
                                 textvariable=student_text, justify='center')
        student_entry.grid(row=9, column=2)
        married_entry = tk.Entry(self, bd=3, font=font, width=9, state='readonly',
                                      textvariable=married_text, justify='center')
        married_entry.grid(row=9, column=3)
        ethnicity_entry = tk.Entry(self, bd=3, font=font, width=14, state='readonly',
                                   textvariable=ethnicity_text, justify='center')
        ethnicity_entry.grid(row=12, column=0)
        old_limit = tk.LabelFrame(self, relief='raised')
        old_limit.grid(row=11, column=3, rowspan=2, sticky='nsew')
        old_limit_text = tk.Label(old_limit, text=limit_text, font=font)
        old_limit_text.pack(expand=True, fill="none")
        self.predict_new_limit()
        self.active_income_button()
        self.check_save_button()

    def predict_new_limit(self):
        self.load_model()
        x_new_rating_scaler = self.scaler_rating.transform(self.current_new_x_rating)
        y_new_rating = self.model_rating.predict(x_new_rating_scaler)
        self.current_new_x_limit[0][1] = y_new_rating
        if y_new_rating < 240:
            rating_y = 0
        elif 240 <= y_new_rating <= 299:
            rating_y = 1
        elif y_new_rating > 299:
            rating_y = 2
        self.current_new_x_limit[0][8] = rating_y
        x_new_limit_scaler = self.scaler_limit.transform(self.current_new_x_limit)
        y_new_limit = self.model_limit.predict(x_new_limit_scaler)
        self.current_new_limit = int(y_new_limit)
        max_limit = tk.LabelFrame(self, relief='raised')
        max_limit.grid(row=14, column=3, rowspan=2, sticky='nsew')
        max_limit_text = tk.Label(max_limit, text=self.current_new_limit, font=font)
        max_limit_text.pack(expand=True, fill="none")
        self.extra_money()

    def extra_money(self):
        if self.current_new_limit - self.old_limit_val < 0:
            self.extra_money_val = 0
        else:
            self.extra_money_val = (self.current_new_limit - self.old_limit_val)
        extra_limit = tk.LabelFrame(self, relief='raised')
        extra_limit.grid(row=17, column=3, rowspan=2, sticky='nsew')
        extra_limit_text = tk.Label(extra_limit, text=self.extra_money_val, font=font)
        extra_limit_text.pack(expand=True, fill="none")


class Options(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.focus_set(self)
        tk.Label(self, text='Ustawienia zaawansowane:', font=large_font).grid(row=0, column=0)
        tk.Label(self, text=' ', font=font).grid(row=1, sticky='nsew')
        tk.Label(self, text=' ', font=font).grid(row=5, sticky='nsew')
        tk.Button(self, text='Menu główne (ESC)', font=font,
                  command=lambda: master.switch_frame(Main)).grid(row=6, column=0, sticky='nsew')
        tk.Frame.bind_all(self, sequence='<Escape>', func=lambda x: master.switch_frame(Main))
        self.popup_warning()
        self.select_model()

    def select_model(self):
        model_label = tk.Label(self, text='Wybierz model:', font=font)
        model_label.grid(row=2, column=0)
        self.model_val = tk.IntVar(self, value=1)
        self.model_1 = tk.Radiobutton(self, text='SVR', command=self.push_model,
                                         font=font, variable=self.model_val, value=1, indicatoron=1)
        self.model_1.grid(row=3, column=0)
        self.model_2 = tk.Radiobutton(self, text='XGBoost', command=self.push_model,
                                        font=font, variable=self.model_val, value=2, indicatoron=1)
        self.model_2.grid(row=4, column=0)
        self.model_1.bind('<Return>', self.select_model_1)
        self.model_2.bind('<Return>', self.select_model_2)

    def push_model(self):
        global model
        model = self.model_val.get()

    def select_model_1(self, model_1):
        self.model_1.invoke()

    def select_model_2(self, model_2):
        self.model_1.invoke()

    def popup_warning(self):
        self.popup = tk.Toplevel()
        tk.Label(self.popup).pack()
        popup_text = 'Uwaga!\nWprowadzone tu zmiany będą miały wpływ\nna otrzymywane wyniki!' \
                     '\nZmian dokonujesz na własne ryzyko.'
        tk.Label(self.popup, text=popup_text, font=font).pack()
        tk.Label(self.popup).pack()
        close = tk.Button(self.popup, text='OK', font=font, command=lambda: self.popup.destroy())
        close.pack()
        close.focus_set()
        close.bind('<Return>', self.popup_destroy)
        tk.Label(self.popup).pack()
        self.popup.geometry('380x160+10+10')
        self.popup.resizable(False, False)
        self.popup.title('Uwaga!')
        self.popup.iconbitmap(icon)
        self.popup.grab_set()

    def popup_destroy(self, popup):
        self.popup.destroy()


if __name__ == '__main__':
    app = Credit()
    app.title('Kalkulator zdolności kredytowej')
    app.geometry('550x600+10+10')
    app.resizable(False, False)
    app.iconbitmap(icon)
    app.mainloop()

# pyinstaller --clean -F -w -i=money.ico --add-data="money.ico;." --add-data="svr_model_limit.joblib;."
# --add-data="svr_model_rating.joblib;." --add-data="svr_scaler_limit.joblib;." --add-data="svr_scaler_rating.joblib;."
# --add-data="CreditNumericOnly.csv;." aplikacja.py
