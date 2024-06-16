import os
import logging
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# Configuração do logging para depuração
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def count_file_extensions(directory, result_text, progress_bar):
    logging.debug(f'Contando extensões de arquivos no diretório: {directory}')
    extensions_set = set()
    total_files = 0

    # Primeiro passo: Contar o número total de arquivos
    for root, _, files in os.walk(directory):
        total_files += len(files)

    processed_files = 0

    # Segundo passo: Coletar extensões e atualizar a barra de progresso
    for root, _, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext:
                extensions_set.add(ext)
            processed_files += 1
            progress_bar["value"] = (processed_files / total_files) * 100
            result_text.update_idletasks()

    logging.debug(f'Extensões únicas encontradas: {extensions_set}')
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Extensões de Arquivo Encontradas:\n")
    for ext in sorted(extensions_set):
        result_text.insert(tk.END, f"{ext}\n")
    result_text.insert(tk.END, f"\nTotal de extensões diferentes: {len(extensions_set)}")
    logging.info('Contagem de extensões concluída.')

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)
        logging.debug(f'Diretório selecionado: {directory}')

def start_count():
    directory = directory_entry.get()
    if os.path.isdir(directory):
        logging.info(f'Iniciando contagem de extensões no diretório: {directory}')
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Contando extensões...\n")
        progress_bar["value"] = 0
        count_thread = threading.Thread(target=count_file_extensions, args=(directory, result_text, progress_bar))
        count_thread.start()
    else:
        messagebox.showerror("Erro", "Por favor, selecione um diretório válido.")
        logging.error("Diretório inválido selecionado")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Contador de Extensões de Arquivo")
logging.debug('Interface gráfica inicializada')

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

directory_label = tk.Label(frame, text="Diretório:")
directory_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

directory_entry = tk.Entry(frame, width=50)
directory_entry.grid(row=0, column=1, padx=5, pady=5)

browse_button = tk.Button(frame, text="Procurar", command=browse_directory)
browse_button.grid(row=0, column=2, padx=5, pady=5)

count_button = tk.Button(frame, text="Contar Extensões", command=start_count)
count_button.grid(row=1, column=0, pady=10)

result_text = scrolledtext.ScrolledText(root, width=80, height=20)
result_text.pack(padx=10, pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(padx=10, pady=5)

root.mainloop()
logging.debug('Execução da interface gráfica concluída')
