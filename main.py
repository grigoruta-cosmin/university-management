from tkinter import * 
from tkinter.messagebox import showerror, showwarning
from tkinter import ttk
import cx_Oracle

root = Tk()
root.title("Managementul unei Facultati")
root.geometry("1920x1080")
tree = ttk.Treeview(root)
entries = []
labels = []
val = IntVar()

#sterge gridurile din frame-ul !!label_name!!
def clear_grid(label_name):
    for l in label_name.grid_slaves():
        l.destroy()

#obtine coloanele din tabelul !!nume_tabel!!
def get_fields(nume_tabel):
    field_names = []
    cursor.execute("select * from " + nume_tabel)
    field_names = [i[0] for i in cursor.description]
    return field_names

#functia generica de submit, primeste coloanele tabelei si numele acestuia
#si insereaza in baza de date
def delete_fct(entries, labels, nume_tabel):
    if nume_tabel.lower() in ('forme_invatamant', 'domenii', 'serii', 'studenti', 'materii'):
        showwarning("Informare", "Ati efectuat operatia de stergere pe un tabel \n cu constrangeri \'ON DELETE CASCADE\'")
    if nume_tabel.lower() == "note":
        string = "DELETE FROM note WHERE ID_STUDENT = " + entries[0].get() + " AND ID_MATERIE = " + entries[1].get() + " AND DATA_EXAMINARE = to_date('" + entries[2].get() + "', 'dd-mon-yyyy')"
        print(string)
        cursor.execute(string)
        c.commit()
        for i in entries:
            i.delete(0, END)
        data_list.delete(0, 'end')
        aux = "SELECT * FROM " + nume_tabel
        cursor.execute(aux)
        rows = cursor.fetchall()
        for item in rows:
            data_list.insert(END, item)
    else:
        string = "DELETE FROM " + nume_tabel + " WHERE " + labels[0].cget("text") + " = \'" + str(prev_pk) + "\'"
        cursor.execute(string)
        c.commit()
        print(string)
        data_list.delete(0, 'end')
        aux = "SELECT * FROM " + nume_tabel
        cursor.execute(aux)
        rows = cursor.fetchall()
        for item in rows:
            data_list.insert(END, item)

def sort_data(nume_tabel, value):
    data_list.delete(0, 'end')
    aux = "SELECT * FROM " + nume_tabel + " ORDER BY " + str(value.get() + 1)
    cursor.execute(aux)
    rows = cursor.fetchall()
    for item in rows:
        data_list.insert(END, item)
    

def sort_radiobuttons(entries, nume_tabel):
    for i in range(len(entries)):
        Radiobutton(radiobuttons_frame, text = labels[i].cget("text"), variable = val, value = i, command = lambda: sort_data(nume_tabel, val)).grid(row = len(entries) + 1, column = i + 2)

def submit_fct(entries, nume_tabel):
    values_string = ""
    for i in range(len(entries)):
        values_string += ":" + str(i) + ","
    comp_list = []
    index_num = 0
    for i in entries:
        comp_list.append((str(index_num), i.get()))
        index_num += 1
    insert_dictionary = {}
    insert_dictionary.update(comp_list)

    aux = "INSERT INTO " + nume_tabel + \
        " VALUES(" + values_string[:len(values_string) - 1] + ")"
    try:
        cursor.execute(aux, insert_dictionary)
    except cx_Oracle.IntegrityError as e:
        errorObj, = e.args
        showerror("Window", str(errorObj.code) + "\n" + errorObj.message)
    else:
        print("Operatiune cu succes")
    c.commit()
    for i in entries:
        i.delete(0, END)
    data_list.delete(0, 'end')
    aux = "SELECT * FROM " + nume_tabel
    cursor.execute(aux)
    rows = cursor.fetchall()
    for item in rows:
        data_list.insert(END, item)

def update_func(entries, labels,nume_tabel):
    values_string = ""
    for i in range(len(entries)):
        values_string += ":" + str(i) + ","
    comp_list = []
    index_num = 0
    for i in entries:
        comp_list.append((str(index_num), i.get()))
        index_num += 1
    update_dictionary = {}
    update_dictionary.update(comp_list)
    print(update_dictionary)
    aux = ""
    index_num = 0
    for i in range(len(labels)):
        aux += labels[i].cget("text") + "=:" + str(index_num) + ","
        index_num += 1
    string = "UPDATE " + nume_tabel + " SET " + aux[:len(aux) - 1] + " WHERE " + labels[0].cget("text") + " = " + "'" + str(prev_pk) + "'"
    print(string)
    print(update_dictionary)
    cursor.execute(string, update_dictionary)
    c.commit()
    data_list.delete(0, 'end')
    aux = "SELECT * FROM " + nume_tabel
    cursor.execute(aux)
    rows = cursor.fetchall()
    for item in rows:
        data_list.insert(END, item)

#functie ce afiseaza intrarile in baza de date a tabelului !!nume_tabel!!
def print_for_entries(field_names, nume_tabel):
    # generate_tree_view(field_names, nume_tabel)
    data_list.delete(0, 'end')
    aux = "SELECT * FROM " + nume_tabel + " ORDER BY 1"
    cursor.execute(aux)
    rows = cursor.fetchall()
    for item in rows:
        data_list.insert(END, item)
    clear_grid(entries_frame)
    clear_grid(radiobuttons_frame)
    global entries
    global labels
    labels = create_labels(field_names)
    entries = create_entries(field_names)
    submit_btn = Button(buttons_frame, text="Insereaza",
                        command=lambda: submit_fct(entries, nume_tabel), width = 10)
    submit_btn.grid(row=0, column= 0)
    update_btn = Button(buttons_frame, text = "Editeaza",
                        command = lambda: update_func(entries, labels, nume_tabel), width = 10)
    update_btn.grid(row = 1, column = 0)
    delete_btn = Button(buttons_frame, text="Sterge",
                        command= lambda: delete_fct(entries, labels, nume_tabel), width = 10)
    delete_btn.grid(row = 2, column = 0)
    sort_radiobuttons(entries, nume_tabel)

def execute_com(string):
    cursor.execute(string)
    data_list.delete(0, "end")
    rows = cursor.fetchall()
    for item in rows:
        data_list.insert(END, item)

def print_for_text():
    #radiobuttons_frame.destroy()
    clear_grid(entries_frame)
    clear_grid(radiobuttons_frame)
    clear_grid(buttons_frame)
    input_text = Text(entries_frame, width = 60, height = 20)
    input_text.grid(row = 0, column = 0)
    submit_btn = Button(buttons_frame, text = "Trimite", command =lambda: execute_com(input_text.get("1.0", END)))
    submit_btn.grid(row = 0, column = 0)

#functie ce creaza numele fiecarei intrari
def create_labels(field_names):
    index_row = 0
    labels = []
    for i in field_names:
        labels.append(Label(entries_frame, text=i))
        labels[index_row].grid(row = index_row, column = 0)
        index_row += 1
    return labels

#functie ce creaza entry-uri pentru fiecare label
def create_entries(field_names):
    index_row = 0
    entries = []
    for i in field_names:
        entries.append(Entry(entries_frame, width=40))
        entries[index_row].grid(row=index_row, column=1, padx = 10, pady = 3)
        index_row += 1
    return entries

def reformat_data(string):
    string = string[:len(string) - 9]
    mon = string[5:7]
    if mon == '01':
        mon = 'JAN'
    elif mon == '02':
        mon = 'FEB'
    elif mon == '03':
        mon = 'MAR'
    elif mon == '04':
        mon = 'APR'
    elif mon == '05':
        mon = 'MAY'
    elif mon == '06':
        mon = 'JUN'
    elif mon == '07':
        mon = 'JUL'
    elif mon == '08':
        mon = 'AUG'
    elif mon == '09':
        mon = 'SEP'
    elif mon == '10':
        mon = 'OCT'
    elif mon == '11':
        mon = 'NOV'
    elif mon == '12':
        mon = 'DEC'
    new_string = string[8:10] + "-" + mon + "-" + string[0:4]
    return new_string

#def executa_comanda()

def select_data(event):
    global selected_item
    index = data_list.curselection()[0]
    selected_item = data_list.get(index)
    index_count = 0
    for i in range(len(entries)):
        entries[i].delete(0, END)
        if labels[i].cget("text").lower() in ('data_finalizare_studii', 'data_nastere', 'data_examinare'):
            entries[i].insert(END, reformat_data(selected_item[index_count]))
        else:    
            entries[i].insert(END, selected_item[index_count])
        index_count += 1
    global prev_pk 
    print(selected_item)
    prev_pk = selected_item[0]
    print(prev_pk)

#conectarea in baza de date
c = cx_Oracle.connect("cosmin", "cosmin1", "localhost/orcl")
cursor = c.cursor()
tables_frame = LabelFrame(root, text="Meniu", padx=5, pady=5)
tables_frame.grid(row=0, column=0)
entries_frame = LabelFrame(root, text="Date")
entries_frame.grid(row = 0, column = 1)
radiobuttons_frame = LabelFrame(root, text="Sorteaza dupa:")
radiobuttons_frame.grid(row = 0, column = 3)

buttons_frame = Label(root)
buttons_frame.grid(row = 0, column = 2)

lista_tabele = ['angajati', 'capacitati', 'departamente', 'domenii',
                'forme_invatamant', 'materii', 'note', 'posturi', 'sali', 'serii', 'studenti']

Button(tables_frame, text = "Angajati", command = lambda: print_for_entries(get_fields("angajati"), "angajati"), width = 14).grid(row = 0, column = 1)
Button(tables_frame, text = "Capacitati", command = lambda: print_for_entries(get_fields("capacitati"), "capacitati"), width = 14).grid(row = 1 , column = 1)
Button(tables_frame, text = "Departamente", command = lambda: print_for_entries(get_fields("departamente"), "departamente"), width = 14).grid(row = 2, column = 1)
Button(tables_frame, text = "Domenii", command = lambda: print_for_entries(get_fields("domenii"), "domenii"), width = 14).grid(row =3, column = 1)
Button(tables_frame, text = "Forme Invatamant", command = lambda: print_for_entries(get_fields("forme_invatamant"), "forme_invatamant"), width = 14).grid(row =4, column = 1)
Button(tables_frame, text = "Materii", command = lambda: print_for_entries(get_fields("materii"), "materii"), width = 14).grid(row =5, column = 1)
Button(tables_frame, text = "Note", command = lambda: print_for_entries(get_fields("note"), "note"), width = 14).grid(row =6, column = 1)
Button(tables_frame, text = "Posturi", command = lambda: print_for_entries(get_fields("posturi"), "posturi"), width = 14).grid(row =7, column = 1)
Button(tables_frame, text = "Sali", command = lambda: print_for_entries(get_fields("sali"), "sali"), width = 14).grid(row =8, column = 1)
Button(tables_frame, text = "Serii", command = lambda: print_for_entries(get_fields("serii"), "serii"), width = 14).grid(row =9, column = 1)
Button(tables_frame, text = "Studenti", command = lambda: print_for_entries(get_fields("studenti"), "studenti"), width = 14).grid(row =10, column = 1)
Button(tables_frame, text = "Interogheaza BD", width = 14, command = print_for_text).grid(row = 11, column = 1)

# input_text = Text(root, width =30, height = 20)
# input_text.grid(row = 2, column = 0)
# Button(root, text = "Executa", command = get_input_text).grid(row = 0, column = 2)

data_list = Listbox(root, height = 25, width = 162)
data_list.grid(row = 1, column = 0, columnspan = 8, rowspan = 6, pady = 20, padx = 20)
scrollbar = Scrollbar(root)
scrollbar.grid(row = 1, column = 8)
data_list.configure(yscroll = scrollbar.set)
scrollbar.configure(command = data_list.yview)
data_list.bind('<<ListboxSelect>>', select_data)
frame_exit = LabelFrame(root, text="Exit frame", padx=10, pady=10)
frame_exit.grid(row=0, column=2)
print(reformat_data("1999-02-15 00:00:00"))
root.mainloop()
