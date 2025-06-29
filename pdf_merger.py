#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 합치기 프로그램 / PDF Merger Program
두 개 이상의 PDF 파일을 하나로 합칩니다.
Merges two or more PDF files into one.
"""

import os
import sys
from PyPDF2 import PdfReader, PdfWriter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class PDFMerger:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF 통합기 / PDF Merger")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 선택된 파일들을 저장할 리스트
        self.selected_files = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """UI 설정 / Setup UI"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="PDF 파일 통합기 / PDF Merger", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 파일 선택 버튼
        select_btn = ttk.Button(main_frame, text="PDF 파일 선택 / Select PDF Files", 
                               command=self.select_files, width=30)
        select_btn.grid(row=1, column=0, pady=5, sticky=tk.W)
        
        # 선택된 파일 목록
        list_frame = ttk.LabelFrame(main_frame, text="선택된 파일들 / Selected Files", padding="5")
        list_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # 리스트박스와 스크롤바
        self.file_listbox = tk.Listbox(list_frame, height=12, width=70)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 버튼 프레임
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        # 파일 제거 버튼
        remove_btn = ttk.Button(btn_frame, text="선택된 파일 제거 / Remove Selected", 
                               command=self.remove_selected)
        remove_btn.grid(row=0, column=0, padx=5)
        
        # 위로 이동 버튼
        up_btn = ttk.Button(btn_frame, text="위로 / Move Up", command=self.move_up)
        up_btn.grid(row=0, column=1, padx=5)
        
        # 아래로 이동 버튼
        down_btn = ttk.Button(btn_frame, text="아래로 / Move Down", command=self.move_down)
        down_btn.grid(row=0, column=2, padx=5)
        
        # 전체 삭제 버튼
        clear_btn = ttk.Button(btn_frame, text="전체 삭제 / Clear All", command=self.clear_all)
        clear_btn.grid(row=0, column=3, padx=5)
        
        # 합치기 버튼
        merge_btn = ttk.Button(main_frame, text="PDF 합치기 / Merge PDFs", 
                              command=self.merge_pdfs, width=30)
        merge_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        # 그리드 설정
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def select_files(self):
        """PDF 파일 선택 / Select PDF files"""
        files = filedialog.askopenfilenames(
            title="PDF 파일을 선택하세요 / Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        for file in files:
            if file not in self.selected_files:
                self.selected_files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))
    
    def remove_selected(self):
        """선택된 파일 제거 / Remove selected file"""
        selection = self.file_listbox.curselection()
        if selection:
            index = selection[0]
            self.file_listbox.delete(index)
            del self.selected_files[index]
    
    def move_up(self):
        """선택된 파일을 위로 이동 / Move selected file up"""
        selection = self.file_listbox.curselection()
        if selection and selection[0] > 0:
            index = selection[0]
            # 리스트에서 순서 변경
            self.selected_files[index-1], self.selected_files[index] = \
                self.selected_files[index], self.selected_files[index-1]
            
            # 리스트박스 업데이트
            self.update_listbox()
            self.file_listbox.selection_set(index-1)
    
    def move_down(self):
        """선택된 파일을 아래로 이동 / Move selected file down"""
        selection = self.file_listbox.curselection()
        if selection and selection[0] < len(self.selected_files) - 1:
            index = selection[0]
            # 리스트에서 순서 변경
            self.selected_files[index], self.selected_files[index+1] = \
                self.selected_files[index+1], self.selected_files[index]
            
            # 리스트박스 업데이트
            self.update_listbox()
            self.file_listbox.selection_set(index+1)
    
    def clear_all(self):
        """모든 파일 삭제 / Clear all files"""
        self.selected_files.clear()
        self.file_listbox.delete(0, tk.END)
    
    def update_listbox(self):
        """리스트박스 업데이트 / Update listbox"""
        self.file_listbox.delete(0, tk.END)
        for file in self.selected_files:
            self.file_listbox.insert(tk.END, os.path.basename(file))
    
    def merge_pdfs(self):
        """PDF 파일들을 합치기 / Merge PDF files"""
        if len(self.selected_files) < 2:
            messagebox.showwarning("경고 / Warning", 
                                 "최소 2개의 PDF 파일을 선택해주세요.\nPlease select at least 2 PDF files.")
            return
        
        # 저장할 파일명 선택
        output_file = filedialog.asksaveasfilename(
            title="합친 PDF를 저장할 위치 선택 / Choose where to save merged PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if not output_file:
            return
        
        try:
            # PDF 합치기 작업
            pdf_writer = PdfWriter()
            
            for file_path in self.selected_files:
                try:
                    with open(file_path, 'rb') as file:
                        pdf_reader = PdfReader(file)
                        
                        # 모든 페이지를 writer에 추가
                        for page in pdf_reader.pages:
                            pdf_writer.add_page(page)
                            
                except Exception as e:
                    messagebox.showerror("오류 / Error", 
                                       f"파일을 읽는 중 오류가 발생했습니다 / Error reading file: {os.path.basename(file_path)}\n{str(e)}")
                    return
            
            # 합친 PDF 저장
            with open(output_file, 'wb') as output:
                pdf_writer.write(output)
            
            messagebox.showinfo("완료 / Complete", 
                              f"PDF 파일이 성공적으로 합쳐졌습니다!\nPDF files merged successfully!\n\n저장 위치 / Saved to: {output_file}")
            
        except Exception as e:
            messagebox.showerror("오류 / Error", 
                               f"PDF를 합치는 중 오류가 발생했습니다.\nError occurred while merging PDFs:\n{str(e)}")
    
    def run(self):
        """프로그램 실행 / Run the program"""
        self.root.mainloop()


def merge_pdfs_command_line(input_files, output_file):
    """
    명령줄에서 PDF 합치기 / Command line PDF merger
    
    Args:
        input_files (list): 입력 PDF 파일 목록 / List of input PDF files
        output_file (str): 출력 파일명 / Output filename
    """
    try:
        pdf_writer = PdfWriter()
        
        for file_path in input_files:
            if not os.path.exists(file_path):
                print(f"오류: 파일을 찾을 수 없습니다 / Error: File not found: {file_path}")
                return False
            
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PdfReader(file)
                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)
                        
                print(f"추가됨 / Added: {os.path.basename(file_path)}")
                        
            except Exception as e:
                print(f"오류: {file_path}를 읽을 수 없습니다 / Error reading {file_path}: {e}")
                return False
        
        # 출력 파일 저장
        with open(output_file, 'wb') as output:
            pdf_writer.write(output)
        
        print(f"\n성공! PDF가 합쳐졌습니다 / Success! PDFs merged: {output_file}")
        return True
        
    except Exception as e:
        print(f"오류: PDF를 합치는 중 문제가 발생했습니다 / Error merging PDFs: {e}")
        return False


def main():
    """메인 함수 / Main function"""
    if len(sys.argv) > 1:
        # 명령줄 모드 / Command line mode
        if len(sys.argv) < 4:
            print("사용법 / Usage: python pdf_merger.py <input1.pdf> <input2.pdf> [input3.pdf ...] <output.pdf>")
            print("예시 / Example: python pdf_merger.py file1.pdf file2.pdf merged.pdf")
            return
        
        input_files = sys.argv[1:-1]  # 마지막 파일을 제외한 모든 파일
        output_file = sys.argv[-1]    # 마지막 파일이 출력 파일
        
        print("PDF 합치기 시작 / Starting PDF merge...")
        print(f"입력 파일들 / Input files: {', '.join([os.path.basename(f) for f in input_files])}")
        print(f"출력 파일 / Output file: {os.path.basename(output_file)}")
        print("-" * 50)
        
        if merge_pdfs_command_line(input_files, output_file):
            print("작업이 완료되었습니다! / Task completed!")
        else:
            print("작업이 실패했습니다. / Task failed.")
    else:
        # GUI 모드 / GUI mode
        app = PDFMerger()
        app.run()


if __name__ == "__main__":
    main() 