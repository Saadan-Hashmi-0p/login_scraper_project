import json
import csv
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from playwright.sync_api import sync_playwright


def run_scraper(login_url, username, password, target_url, selector, output_format):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            # Go to login page and login
            page.goto(login_url)
            page.fill('input#ap_email', username)
            page.fill('input#ap_password', password)
            page.click('input#signInSubmit')

            page.wait_for_timeout(3000)

            # Go to target page
            page.goto(target_url)
            page.wait_for_timeout(3000)


            # Scrape content
            elements = page.query_selector_all(selector)
            data = []

            for el in elements:
                text = el.inner_text().strip()
                if text:
                    data.append({"name": text})

            if output_format == "JSON":
                with open("output.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                saved_file = "output.json"

            elif output_format == "CSV":
                with open("output.csv", "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=["text"])
                    writer.writeheader()
                    writer.writerows(data)
                saved_file = "output.csv"
            elif output_format == "Text":
             with open("output.txt", "w", encoding="utf-8") as f:
                 with open("output.txt", "w", encoding="utf-8") as f:
                     for row in data:
                        f.write(f"name: {row['name']}\n")
                        saved_file = "output.txt"

                    


            browser.close()
            messagebox.showinfo("Done", f" Scraped {len(data)} items.\nSaved to {saved_file}")

    except Exception as e:
        messagebox.showerror("Error", f" {str(e)}")


def start_scraping():
    login_url = login_url_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    target_url = target_url_entry.get()
    selector = selector_entry.get()
    output_format = output_format_var.get()

    if not all([login_url, username, password, target_url, selector]):
        messagebox.showwarning("Missing Input", "Please fill all fields.")
        return

    threading.Thread(
        target=run_scraper,
        args=(login_url, username, password, target_url, selector, output_format),
        daemon=True
    ).start()


# GUI Setup
root = tk.Tk()
root.title("Dynamic Web Scraper with Login")
root.geometry("450x400")

tk.Label(root, text=" Login URL").pack()
login_url_entry = tk.Entry(root, width=55)
login_url_entry.pack()

tk.Label(root, text=" Username").pack()
username_entry = tk.Entry(root, width=55)
username_entry.pack()

tk.Label(root, text=" Password").pack()
password_entry = tk.Entry(root, width=55, show="*")
password_entry.pack()

tk.Label(root, text=" Target Page URL to Scrape").pack()
target_url_entry = tk.Entry(root, width=55)
target_url_entry.pack()

tk.Label(root, text=" HTML Tag or CSS Selector (e.g. p, div.card)").pack()
selector_entry = tk.Entry(root, width=55)
selector_entry.pack()

tk.Label(root, text=" Output Format").pack()
output_format_var = tk.StringVar(value="JSON")
ttk.Combobox(root, textvariable=output_format_var, values=["JSON", "CSV","Text"], state="readonly", width=52).pack()

tk.Button(root, text="Run Scraper", command=start_scraping, bg="#2196F3", fg="white").pack(pady=15)

root.mainloop()   